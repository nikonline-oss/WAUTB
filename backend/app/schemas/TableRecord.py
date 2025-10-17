# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime


class TableRecordBase(BaseModel):
    data: Dict[str, Any]

class TableRecordCreate(TableRecordBase):
    pass

class TableRecordResponse(TableRecordBase):
    id: int
    table_template_id: int
    created_by: int
    updated_by: int
    created_at: datetime
    updated_at: datetime
    version: int
    
    class Config:
        from_attributes = True