# schemas/excel.py
from pydantic import BaseModel
from typing import Dict, List, Any, Optional

class ExcelImportRequest(BaseModel):
    table_template_id: int
    mapping: Dict[str, str]  # {column_name: excel_column_name}
    skip_first_rows: int = 0

class ExcelImportResponse(BaseModel):
    success: bool
    imported_records: int
    errors: List[Dict[str, Any]] = []
    message: str = ""

class ExcelPreviewResponse(BaseModel):
    columns: List[str]
    preview_data: List[Dict[str, Any]]
    suggested_mapping: Dict[str, str]
    table_columns: List[Dict[str, Any]]

class ExcelCreateTableRequest(BaseModel):
    table_name: str
    skip_first_rows: int = 0