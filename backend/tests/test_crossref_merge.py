import pytest
from app.services.crossref_service import CrossrefService

@pytest.fixture
def service():
    return CrossrefService()

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
