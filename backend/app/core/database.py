import sqlite3
import os
import json
import uuid
from datetime import datetime
from fastapi import HTTPException
from app.core.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "local.db"
)

_connection: sqlite3.Connection | None = None


def _get_conn() -> sqlite3.Connection:
    global _connection
    if _connection is None:
        _connection = sqlite3.connect(DB_PATH, check_same_thread=False)
        _connection.row_factory = sqlite3.Row
        _init_tables()
    return _connection


def _init_tables():
    conn = _get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS templates (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            columns TEXT DEFAULT '[]',
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS rules (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT DEFAULT '',
            conditions TEXT DEFAULT '[]',
            action TEXT DEFAULT '{}',
            enabled INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS extraction_results (
            id TEXT PRIMARY KEY,
            template_id TEXT,
            filename TEXT,
            status TEXT DEFAULT 'ok',
            data TEXT DEFAULT '{}',
            created_at TEXT DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    logger.info("Base de datos SQLite inicializada")


class QueryResult:
    def __init__(self, data: list[dict]):
        self.data = data


class QueryBuilder:
    def __init__(self, table: str, method: str = "select"):
        self._table = table
        self._method = method
        self._columns = "*"
        self._filters: list[tuple[str, str, object]] = []
        self._insert_data: dict | None = None
        self._update_data: dict | None = None

    def select(self, columns: str = "*"):
        self._method = "select"
        self._columns = columns
        return self

    def insert(self, data: dict):
        self._method = "insert"
        self._insert_data = data
        return self

    def update(self, data: dict):
        self._method = "update"
        self._update_data = data
        return self

    def delete(self):
        self._method = "delete"
        return self

    def eq(self, field: str, value: object):
        self._filters.append(("eq", field, value))
        return self

    def _serialize(self, data: dict) -> dict:
        d = {}
        for k, v in data.items():
            if isinstance(v, bool):
                d[k] = 1 if v else 0
            elif isinstance(v, (list, dict)):
                d[k] = json.dumps(v, ensure_ascii=False)
            else:
                d[k] = v
        return d

    def _deserialize(self, row: dict) -> dict:
        d = {}
        for k, v in row.items():
            if v is None:
                d[k] = v
            elif isinstance(v, str):
                try:
                    parsed = json.loads(v)
                    d[k] = parsed
                except (json.JSONDecodeError, TypeError):
                    d[k] = v
            elif isinstance(v, int):
                d[k] = bool(v) if v in (0, 1) else v
            else:
                d[k] = v
        return d

    def execute(self) -> QueryResult:
        conn = _get_conn()
        cur = conn.cursor()

        if self._method == "select":
            sql = f"SELECT {self._columns} FROM {self._table}"
            params: list[object] = []
            if self._filters:
                conds = []
                for op, field, val in self._filters:
                    if op == "eq":
                        conds.append(f"{field} = ?")
                        params.append(1 if val is True else (0 if val is False else val))
                if conds:
                    sql += " WHERE " + " AND ".join(conds)
            cur.execute(sql, params)
            rows = [self._deserialize(dict(row)) for row in cur.fetchall()]
            return QueryResult(rows)

        elif self._method == "insert":
            data = dict(self._insert_data) if self._insert_data else {}
            if "id" not in data:
                data["id"] = str(uuid.uuid4())
            now = datetime.now().isoformat()
            data.setdefault("created_at", now)
            data.setdefault("updated_at", now)
            serialized = self._serialize(data)
            cols = ", ".join(serialized.keys())
            ph = ", ".join("?" for _ in serialized)
            cur.execute(
                f"INSERT INTO {self._table} ({cols}) VALUES ({ph})",
                list(serialized.values())
            )
            conn.commit()
            return QueryResult([self._deserialize(serialized)])

        elif self._method == "update":
            data = dict(self._update_data) if self._update_data else {}
            data["updated_at"] = datetime.now().isoformat()
            serialized = self._serialize(data)
            params: list[object] = list(serialized.values())
            set_clause = ", ".join(f"{k} = ?" for k in serialized)
            for op, field, val in self._filters:
                if op == "eq":
                    params.append(1 if val is True else (0 if val is False else val))
            where_conds = []
            for op, field, _ in self._filters:
                if op == "eq":
                    where_conds.append(f"{field} = ?")
            sql = f"UPDATE {self._table} SET {set_clause}"
            if where_conds:
                sql += " WHERE " + " AND ".join(where_conds)
            cur.execute(sql, params)
            conn.commit()
            return QueryResult([])

        elif self._method == "delete":
            sql = f"DELETE FROM {self._table}"
            params = []
            if self._filters:
                conds = []
                for op, field, val in self._filters:
                    if op == "eq":
                        conds.append(f"{field} = ?")
                        params.append(1 if val is True else (0 if val is False else val))
                if conds:
                    sql += " WHERE " + " AND ".join(conds)
            cur.execute(sql, params)
            conn.commit()
            return QueryResult([])

        return QueryResult([])


class LocalSupabaseClient:
    def table(self, name: str) -> QueryBuilder:
        return QueryBuilder(name)


_client: LocalSupabaseClient | None = None


def get_supabase() -> LocalSupabaseClient | None:
    global _client
    if _client is None:
        _client = LocalSupabaseClient()
        logger.info("Usando SQLite local")
    return _client


def require_supabase() -> LocalSupabaseClient:
    client = get_supabase()
    if client is None:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    return client


class Database:
    def __init__(self):
        self.connection = None

    async def connect(self):
        logger.info("Conectando a base de datos local...")
        _init_tables()
        logger.info("Base de datos local conectada")

    async def disconnect(self):
        logger.info("Desconectando de base de datos local...")
        global _connection, _client
        if _connection:
            _connection.close()
            _connection = None
        _client = None


db = Database()


async def init_db():
    await db.connect()
