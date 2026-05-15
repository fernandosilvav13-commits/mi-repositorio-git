# Phase 04: Cross-Reference Export - Pattern Map

**Mapped:** 2026-05-15
**Files analyzed:** 4
**Analogs found:** 4 / 4

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `backend/app/services/crossref_service.py` | service | transform | `backend/app/services/consolidator.py` | role-match |
| `backend/app/services/excel_service.py` | service | transform/file-I/O | Itself (existing `generate`) | exact |
| `backend/app/api/export.py` | controller | request-response | Itself (existing `export_to_excel`) | exact |
| `backend/app/schemas/crossref.py` | schema | transform | `backend/app/schemas/rules.py` | role-match |

## Pattern Assignments

### `backend/app/services/crossref_service.py` (service, transform)

**Analog:** `backend/app/services/consolidator.py`

**Merge logic with compound keys** (Target pattern):
```python
def merge_data(self, rows, crossref_rows, match_keys, output_columns):
    # match_keys: [{"extractionKey": "k1", "crossrefKey": "c1"}, ...]
    ext_keys = [m["extractionKey"] for m in match_keys]
    ref_keys = [m["crossrefKey"] for m in match_keys]
    
    # 1. Build lookup with tuple keys (O(N))
    lookup = {}
    for cr_row in crossref_rows:
        key = tuple(str(cr_row.get(k, "")).strip().lower() for k in ref_keys)
        if any(key): # Only index if at least one key is present
            lookup[key] = cr_row
            
    # 2. Merge with extraction rows (O(M))
    merged = []
    for row in rows:
        new_row = dict(row)
        row_key = tuple(str(row.get(k, "")).strip().lower() for k in ext_keys)
        matched = lookup.get(row_key)
        
        if matched:
            for col in output_columns:
                new_row[col] = matched.get(col, "")
        else:
            for col in output_columns:
                new_row[col] = "NO ENCONTRADO"
        merged.append(new_row)
    return merged
```

---

### `backend/app/services/excel_service.py` (service, transform/file-I/O)

**Analog:** Itself (existing `generate` method)

**Visual Flagging and Header Prefixing** (lines 35-53):
```python
# Header prefixing pattern
for col_idx, col_name in enumerate(columns, 1):
    display_name = f"[REF] {col_name}" if col_name in crossref_columns else col_name
    cell = ws.cell(row=1, column=col_idx, value=display_name)
    cell.fill = header_fill
    # ...

# Row highlighting pattern
for row_idx, row_data in enumerate(rows, 2):
    # Detection: row is unmatched if all crossref columns are "NO ENCONTRADO"
    is_unmatched = crossref_columns and all(
        row_data.get(col) == "NO ENCONTRADO" for col in crossref_columns
    )
    
    if is_unmatched:
        for col_idx in range(1, len(columns) + 1):
            ws.cell(row=row_idx, column=col_idx).fill = YELLOW_FILL
```

---

### `backend/app/api/export.py` (controller, request-response)

**Analog:** Itself (existing entry point)

**Orchestration Pattern** (lines 43-68):
```python
# Handle new matchKeys structure
if crossref_file_id and column_mapping:
    # ... manifest lookup ...
    match_keys = column_mapping.get("matchKeys", [])
    output_columns = column_mapping.get("output_columns", [])
    
    full_data = crossref_service.load_file_data(entry["name"])
    merged_rows = crossref_service.merge_data(
        rows=consolidated_rows,
        crossref_rows=full_data,
        match_keys=match_keys,
        output_columns=output_columns,
    )
    # ... update columns ...
```

---

### `backend/app/schemas/crossref.py` (schema, transform)

**Analog:** `backend/app/schemas/rules.py`

**Nested Object Pattern**:
```python
class MatchKey(BaseModel):
    extractionKey: str
    crossrefKey: str

class ColumnMapping(BaseModel):
    matchKeys: list[MatchKey]
    output_columns: list[str]
```

## Shared Patterns

### Dictionary-based Lookup
**Source:** `backend/app/services/consolidator.py`
**Apply to:** `CrossrefService.merge_data`
Use tuples for keys when multiple columns are involved in a match to ensure O(1) performance.

### Conditional Styling
**Source:** `backend/app/services/excel_service.py`
**Apply to:** Row highlighting in `generate`
Use `openpyxl.styles.PatternFill` for color-based flagging of data quality issues.

## No Analog Found

All files have direct analogs or are existing files being extended.

## Metadata

**Analog search scope:** `backend/app/`
**Files scanned:** 40
**Pattern extraction date:** 2026-05-15
