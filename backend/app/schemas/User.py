# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime
from ..schemas.TableTemplate import TableTemplateResponse
# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
class UserResponseWithTemplates(UserResponse):
    created_templates: List[TableTemplateResponse] = []  # Шаблоны пользователя

    class Config:
        from_attributes = True