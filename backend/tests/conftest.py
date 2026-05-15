import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Test client for FastAPI."""
    return TestClient(app)

@pytest.fixture
def mock_db():
    """Mock Supabase client."""
    # This will be refined if needed
    return None

@pytest.fixture
def mock_crossref_data():
    """Example cross-reference data."""
    return [
        {"RUT": "12.345.678-9", "Nombre": "Juan Perez", "Cargo": "Analista"},
        {"RUT": "11.222.333-4", "Nombre": "Maria Garcia", "Cargo": "Desarrollador"},
    ]
