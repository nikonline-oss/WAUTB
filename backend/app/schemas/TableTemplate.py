# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime
from .TableColumn import TableColumnCreate, TableColumnResponse


class TableTemplateBase(BaseModel):
    name: str

class TableTemplateCreate(TableTemplateBase):
    pass

class TableTemplateUpdate(TableTemplateBase):
    pass

class TableTemplateResponse(TableTemplateBase):
    id: int
    created_at: datetime
    updated_at: datetime

    columns: List[TableColumnResponse] = []
    class Config:
        from_attributes = True