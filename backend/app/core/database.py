from fastapi import HTTPException
from supabase import create_client, Client
from app.core.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

supabase: Client | None = None


def get_supabase() -> Client | None:
    global supabase
    if supabase is None:
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            logger.warning("SUPABASE_URL o SUPABASE_KEY no configurados")
            return None
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        logger.info("Conectado a Supabase")
    return supabase


def require_supabase() -> Client:
    client = get_supabase()
    if client is None:
        raise HTTPException(
            status_code=503,
            detail="Base de datos no disponible. Configura SUPABASE_URL y SUPABASE_KEY en el .env",
        )
    return client


class Database:
    def __init__(self):
        self.connection = None

    async def connect(self):
        logger.info("Conectando a base de datos...")
        client = get_supabase()
        if client:
            self.connection = client
            logger.info("Base de datos conectada")
        else:
            logger.warning("Base de datos no disponible")

    async def disconnect(self):
        logger.info("Desconectando de base de datos...")
        self.connection = None
        logger.info("Base de datos desconectada")


db = Database()


async def init_db():
    await db.connect()
