# schemas/permission.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class UserTablePermissionBase(BaseModel):
    user_id: int
    table_template_id: int
    can_view: bool = False
    can_add_rows: bool = False
    can_edit_rows: bool = False
    can_delete_rows: bool = False
    can_edit_structure: bool = False
    can_add_table: bool = False

class UserTablePermissionCreate(UserTablePermissionBase):
    pass

class UserTablePermissionUpdate(BaseModel):
    can_view: Optional[bool] = None
    can_add_rows: Optional[bool] = None
    can_edit_rows: Optional[bool] = None
    can_delete_rows: Optional[bool] = None
    can_edit_structure: Optional[bool] = None
    can_add_table: Optional[bool] = None

class UserTablePermissionResponse(UserTablePermissionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Схемы для массового управления правами
class BulkPermissionUpdate(BaseModel):
    user_id: int
    table_template_ids: List[int]
    permissions: UserTablePermissionUpdate

class UserWithPermissions(BaseModel):
    id: int
    email: str
    lastname: str
    firstname: str
    middlename: str
    department_id: int
    role: str
    permissions: List[UserTablePermissionResponse] = []

    class Config:
        from_attributes = True