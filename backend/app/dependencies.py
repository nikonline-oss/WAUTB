from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Optional

from .schemas import user as schemas
from .database import get_db
from .crud.user import user_repository as user_repo
from .core.config import settings
from .services.permission_service import PermissionService, get_permission_service

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> schemas.UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверные учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: Optional[str] = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = user_repo.get_by_id(db, int(user_id))
    if user is None:
        raise credentials_exception
    
    return schemas.UserResponse.model_validate(user)

async def get_current_active_user(current_user: schemas.UserResponse = Depends(get_current_user)):
    """Получение текущего активного пользователя"""
    return current_user

# Для проверки прав администратора
async def get_admin_user(current_user: schemas.UserResponse = Depends(get_current_user)):
    """Проверка прав администратора"""
    # if not current_user.is_admin:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Недостаточно прав"
    #     )
    return current_user

async def check_table_permission(
    table_template_id: int,
    permission_type: str,
    current_user = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service)
):
    """Зависимость для проверки прав доступа к таблице"""
    has_permission = permission_service.check_permission(
        current_user.id, table_template_id, permission_type
    )
    
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения операции"
        )
    
    return current_user

# Конкретные зависимости для разных типов прав
async def check_view_permission(table_template_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await check_table_permission(table_template_id, 'view', current_user, db)

async def check_add_rows_permission(table_template_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await check_table_permission(table_template_id, 'add_rows', current_user, db)

async def check_edit_rows_permission(table_template_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await check_table_permission(table_template_id, 'edit_rows', current_user, db)

async def check_delete_rows_permission(table_template_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await check_table_permission(table_template_id, 'delete_rows', current_user, db)

async def check_edit_structure_permission(table_template_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await check_table_permission(table_template_id, 'edit_structure', current_user, db)

# Зависимость для проверки админских прав
async def get_admin_user(current_user = Depends(get_current_user)):
    """Проверка прав администратора"""
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав. Требуются права администратора"
        )
    return current_user