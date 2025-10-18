from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

class DepartmentBase(BaseModel):
    title: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class DepartmentWithUsers(DepartmentResponse):
    users: List['UserResponse'] = []

class DepartmentUpdate(BaseModel):
    title: Optional[str] = None