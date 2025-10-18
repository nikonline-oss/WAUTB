from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ..dependencies import get_current_active_user
from ..schemas import user as schemas
from ..services.user_services import UserService, get_user_service
from ..services.auth_service import create_access_token
from ..core.config import settings

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post(
    "/login",
    summary="Аутентификация",
    description="Аутентификация пользователя и получение JWT токена"
)
def login(
    form_data: schemas.UserLogin,
    user_service: UserService = Depends(get_user_service)
):
    user = user_service.authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.post(
    "/register", 
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация",
    description="Регистрация нового пользователя в системе"
)
def register(
    user_data: schemas.UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    return user_service.create_user(user_data)

@router.post(
    "/refresh",
    summary="Обновление токена",
    description="Обновление JWT токена (если нужно)"
)
def refresh_token(current_user: schemas.UserResponse = Depends(get_current_active_user)):
    # Логика обновления токена
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(current_user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }