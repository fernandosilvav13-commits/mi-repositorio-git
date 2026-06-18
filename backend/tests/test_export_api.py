import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def _setup_manifest():
    manifest_dir = Path("uploads/crossref")
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / "manifest.json"
    manifest_path.write_text(json.dumps([
        {"id": "mock-file-id", "name": "mock_crossref.csv"}
    ]))
    yield
    if manifest_path.exists():
        manifest_path.unlink()


def test_export_api_with_compound_match_keys(_setup_manifest):
    """
    Test the /api/export/ endpoint with the new matchKeys structure.
    """
    payload = {
        "template_id": "mock-template-id",
        "rows": [{"Nombre": "Juan", "Apellido": "Perez", "RUT": "12.345.678-9"}],
        "crossref_file_id": "mock-file-id",
        "column_mapping": {
            "matchKeys": [
                {"local": "Nombre", "remote": "First Name"},
                {"local": "Apellido", "remote": "Last Name"}
            ],
            "output_columns": ["Email"]
        }
    }

    with (
        patch("app.api.export.require_supabase") as mock_supa,
        patch("app.api.export.crossref_service.load_file_data") as mock_load,
    ):
        mock_supa.return_value.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
            {"id": "mock-template-id", "columns": [{"name": "Nombre"}, {"name": "Apellido"}, {"name": "RUT"}]}
        ]
        mock_load.return_value = [
            {"First Name": "Juan", "Last Name": "Perez", "Email": "juan@example.com"}
        ]

        response = client.post("/api/export/", json=payload)
        assert response.status_code == 200

def test_export_api_missing_required_fields():
    """Test validation of required fields."""
    response = client.post("/api/export/", json={})
    assert response.status_code == 400
    assert "template_id y rows son requeridos" in response.json()["detail"]
