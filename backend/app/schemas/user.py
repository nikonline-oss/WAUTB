from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from .department import DepartmentResponse

class UserBase(BaseModel):
    email: EmailStr
    lastname: str
    firstname: str
    middlename: str = ""
    department_id: int

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    lastname: Optional[str] = None
    firstname: Optional[str] = None
    middlename: Optional[str] = None
    department_id: Optional[int] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserWithDepartment(UserResponse):
    department: Optional[DepartmentResponse] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str


UserResponse.model_rebuild()