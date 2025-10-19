# routers/permission.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from ..services.permission_service import PermissionService, get_permission_service
from ..schemas.permission import (
    UserTablePermissionCreate, UserTablePermissionUpdate, UserTablePermissionResponse,
    BulkPermissionUpdate, UserWithPermissions
)
from ..dependencies import get_admin_user

router = APIRouter(prefix="/permissions", tags=["permissions"])

@router.post("/", response_model=UserTablePermissionResponse, dependencies=[Depends(get_admin_user)])
def create_permission(
    permission_data: UserTablePermissionCreate,
    service: PermissionService = Depends(get_permission_service)
):
    """Создание права доступа (только для администраторов)"""
    return service.set_user_permission(permission_data)

@router.get("/user/{user_id}", response_model=List[UserTablePermissionResponse], dependencies=[Depends(get_admin_user)])
def get_user_permissions(
    user_id: int,
    service: PermissionService = Depends(get_permission_service)
):
    """Получение всех прав пользователя (только для администраторов)"""
    return service.get_user_permissions(user_id)

@router.get("/user/{user_id}/full", response_model=UserWithPermissions, dependencies=[Depends(get_admin_user)])
def get_user_with_permissions(
    user_id: int,
    service: PermissionService = Depends(get_permission_service)
):
    """Получение пользователя со всеми правами (только для администраторов)"""
    return service.get_user_with_permissions(user_id)

@router.get("/table/{table_template_id}", response_model=List[UserTablePermissionResponse], dependencies=[Depends(get_admin_user)])
def get_table_permissions(
    table_template_id: int,
    service: PermissionService = Depends(get_permission_service)
):
    """Получение всех прав на таблицу (только для администраторов)"""
    return service.get_table_permissions(table_template_id)

@router.put("/{permission_id}", response_model=UserTablePermissionResponse, dependencies=[Depends(get_admin_user)])
def update_permission(
    permission_id: int,
    permission_data: UserTablePermissionUpdate,
    service: PermissionService = Depends(get_permission_service)
):
    """Обновление права доступа (только для администраторов)"""
    return service.update_user_permission(permission_id, permission_data)

# @router.post("/bulk", response_model=List[UserTablePermissionResponse], dependencies=[Depends(get_admin_user)])
# def bulk_update_permissions(
#     bulk_data: BulkPermissionUpdate,
#     service: PermissionService = Depends(get_permission_service)
# ):
#     """Массовое обновление прав (только для администраторов)"""
#     return service.bulk_update_permissions(bulk_data)
