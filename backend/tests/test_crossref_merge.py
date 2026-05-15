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
    """
    Test merging data using multiple columns as match keys.
    Currently, merge_data only supports a single match_column.
    This test is expected to fail or need adjustment once compound keys are supported.
    """
    rows = [
        {"Nombre": "Juan", "Apellido": "Perez", "ID": "1"},
        {"Nombre": "Maria", "Apellido": "Garcia", "ID": "2"},
    ]
    crossref_rows = [
        {"First": "Juan", "Last": "Perez", "Email": "juan@example.com"},
        {"First": "Maria", "Last": "Garcia", "Email": "maria@example.com"},
    ]
    
    # This represents the desired new API structure (to be implemented)
    match_keys = [
        {"local": "Nombre", "remote": "First"},
        {"local": "Apellido", "remote": "Last"}
    ]
    output_columns = ["Email"]
    
    # Expecting to fail because the current merge_data doesn't take match_keys list
    with pytest.raises(TypeError):
        service.merge_data(
            rows=rows,
            crossref_rows=crossref_rows,
            match_keys=match_keys,
            output_columns=output_columns
        )

def test_merge_data_normalization(service):
    """Test that matching is case-insensitive and ignores extra whitespace."""
    rows = [{"RUT": " 12.345.678-9 "}]
    crossref_rows = [{"rut_ref": "12.345.678-9", "Data": "Found"}]
    
    # Current single column API
    merged = service.merge_data(
        rows=rows,
        crossref_rows=crossref_rows,
        match_column="RUT",
        crossref_match_column="rut_ref",
        output_columns=["Data"]
    )
    
    assert merged[0]["Data"] == "Found"
