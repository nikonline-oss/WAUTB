# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime
from .TableColumn import TableColumnCreate


class TableTemplateBase(BaseModel):
    name: str

class TableTemplateCreate(TableTemplateBase):
    columns: List[TableColumnCreate] = []

class TableTemplateResponse(TableTemplateBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True