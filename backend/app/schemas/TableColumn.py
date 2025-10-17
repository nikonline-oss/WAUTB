# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime

class TableColumnBase(BaseModel):
    name: str
    data_type: str
    order_index: int = 0
    config: Dict[str, Any] = {}

class TableColumnCreate(TableColumnBase):
    pass

class TableColumnResponse(TableColumnBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True