import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

from unittest.mock import patch, MagicMock

def test_export_api_with_compound_match_keys(client):
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
    
    with patch("app.api.export.require_supabase") as mock_supa:
        # Mock template data
        mock_supa.return_value.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
            {"id": "mock-template-id", "columns": [{"name": "Nombre"}, {"name": "Apellido"}, {"name": "RUT"}]}
        ]
        
        # This will fail because 'match_column' is missing in column_mapping
        response = client.post("/api/export/", json=payload)
        
        # We expect a KeyError or similar if it tries to access column_mapping['match_column']
        assert response.status_code == 500 or response.status_code == 400

def test_export_api_missing_required_fields(client):
    """Test validation of required fields."""
    response = client.post("/api/export/", json={})
    assert response.status_code == 400
    assert "template_id y rows son requeridos" in response.json()["detail"]
