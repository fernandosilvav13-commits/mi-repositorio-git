import pytest
from app.services.crossref_service import CrossrefService

from app.schemas.crossref import ColumnMapping, MatchKey

@pytest.fixture
def service():
    return CrossrefService()

def test_schema():
    """Verify that ColumnMapping validates the Wizard payload format."""
    payload = {
        "matchKeys": [{"extractionKey": "k1", "crossrefKey": "c1"}],
        "output_columns": ["col1"]
    }
    mapping = ColumnMapping(**payload)
    assert len(mapping.matchKeys) == 1
    assert mapping.matchKeys[0].extractionKey == "k1"
    assert mapping.matchKeys[0].crossrefKey == "c1"
    assert mapping.output_columns == ["col1"]

def test_merge_data_compound_keys(service):
    """Test merging data using multiple columns as match keys."""
    rows = [
        {"Nombre": "Juan", "Apellido": "Perez", "ID": "1"},
        {"Nombre": "Maria", "Apellido": "Garcia", "ID": "2"},
    ]
    crossref_rows = [
        {"First": "Juan", "Last": "Perez", "Email": "juan@example.com"},
        {"First": "Maria", "Last": "Garcia", "Email": "maria@example.com"},
    ]
    
    match_keys = [
        {"extractionKey": "Nombre", "crossrefKey": "First"},
        {"extractionKey": "Apellido", "crossrefKey": "Last"}
    ]
    output_columns = ["Email"]
    
    merged = service.merge_data(
        rows=rows,
        crossref_rows=crossref_rows,
        match_keys=match_keys,
        output_columns=output_columns
    )
    
    assert merged[0]["Email"] == "juan@example.com"
    assert merged[1]["Email"] == "maria@example.com"

def test_merge_data_normalization(service):
    """Test that matching is case-insensitive and ignores extra whitespace."""
    rows = [{"RUT": " 12.345.678-9 "}]
    crossref_rows = [{"rut_ref": "12.345.678-9", "Data": "Found"}]
    
    match_keys = [{"extractionKey": "RUT", "crossrefKey": "rut_ref"}]
    
    merged = service.merge_data(
        rows=rows,
        crossref_rows=crossref_rows,
        match_keys=match_keys,
        output_columns=["Data"]
    )
    
    assert merged[0]["Data"] == "Found"

def test_merge_data_unmatched(service):
    """Test that unmatched rows have 'NO ENCONTRADO' in output columns."""
    rows = [{"RUT": "1-1"}]
    crossref_rows = [{"rut_ref": "2-2", "Data": "Other"}]
    
    match_keys = [{"extractionKey": "RUT", "crossrefKey": "rut_ref"}]
    
    merged = service.merge_data(
        rows=rows,
        crossref_rows=crossref_rows,
        match_keys=match_keys,
        output_columns=["Data"]
    )
    
    assert merged[0]["Data"] == "NO ENCONTRADO"
