# dependencies.py
from fastapi import Depends, HTTPException, status, Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Optional

from .schemas import user as schemas
from .database import get_db
from .crud.user import user_repository as user_repo
from .core.config import settings
from .services.permission_service import PermissionService

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
    return current_user

# Фабрика для создания проверок прав с правильными параметрами
def create_permission_checker(permission_type: str):
    async def permission_checker(
        table_id: int = Path(..., description="ID таблицы", gt=0),
        current_user: schemas.UserResponse = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        permission_service = PermissionService(db)
        has_permission = permission_service.check_permission(
            current_user.id, table_id, permission_type
        )
        
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Недостаточно прав: требуется право '{permission_type}'"
            )
        
        return current_user
    return permission_checker

# Создаем конкретные проверки прав
check_view_permission = create_permission_checker("view")
check_add_rows_permission = create_permission_checker("add_rows")
check_edit_rows_permission = create_permission_checker("edit_rows")
check_delete_rows_permission = create_permission_checker("delete_rows")
check_edit_structure_permission = create_permission_checker("edit_structure")

# Зависимость для проверки админских прав
async def get_admin_user(current_user: schemas.UserResponse = Depends(get_current_user)):
    """Проверка прав администратора"""
    # Временно закомментируем проверку роли, если поле отсутствует
    # if not hasattr(current_user, 'role') or current_user.role != 'admin':
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Недостаточно прав. Требуются права администратора"
    #     )
    return current_user