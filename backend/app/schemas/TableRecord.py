# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime
from ..schemas.TableTemplate import TableTemplateResponse

class TableRecordBase(BaseModel):
    data: Dict[str, Any]

class TableRecordCreate(TableRecordBase):
    table_template_id: int

class TableRecordUpdate(TableRecordBase):
    pass

class TableRecordResponse(TableRecordBase):
    id: int
    table_template_id: int
    created_at: datetime
    updated_at: datetime
    table_template: Optional[TableTemplateResponse] = None

    class Config:
        from_attributes = True