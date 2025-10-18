# schemas/table.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List

# TableColumn Schemas
class TableColumnBase(BaseModel):
    name: str
    data_type: str
    order_index: int = 0
    config: Dict[str, Any] = {}

class TableColumnCreate(TableColumnBase):
    table_template_id: int

class TableColumnUpdate(BaseModel):
    name: Optional[str] = None
    data_type: Optional[str] = None
    order_index: Optional[int] = None
    config: Optional[Dict[str, Any]] = None

class TableColumnResponse(TableColumnBase):
    id: int
    table_template_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# TableTemplate Schemas
class TableTemplateBase(BaseModel):
    name: str

class TableTemplateCreate(TableTemplateBase):
    pass

class TableTemplateUpdate(BaseModel):
    name: Optional[str] = None

class TableTemplateResponse(TableTemplateBase):
    id: int
    created_at: datetime
    updated_at: datetime
    columns: List[TableColumnResponse] = []

    class Config:
        from_attributes = True

# TableRecord Schemas
class TableRecordBase(BaseModel):
    table_template_id: int
    data: Dict[str, Any]

class TableRecordCreate(TableRecordBase):
    pass

class TableRecordUpdate(BaseModel):
    data: Optional[Dict[str, Any]] = None

class TableRecordResponse(TableRecordBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True