from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Optional

from .schemas import user as schemas
from .database import get_db
from .crud.user import user_repository as user_repo
from .core.config import settings
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