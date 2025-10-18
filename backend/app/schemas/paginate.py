# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime


class FilterCondition(BaseModel):
    field: str
    operator: str  # 'eq', 'ne', 'gt', 'lt', 'gte', 'lte', 'like', 'in', 'contains'
    value: Any

class SortCondition(BaseModel):
    field: str
    direction: str  # 'asc', 'desc'

class PaginatedRequest(BaseModel):
    page: int = 1
    per_page: int = 50
    filters: List[FilterCondition] = []
    sort: List[SortCondition] = []
    search: Optional[str] = None

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    per_page: int
    total_pages: int

    class Config:
        from_attributes = True