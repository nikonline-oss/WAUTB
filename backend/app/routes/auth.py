from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta

from ..schemas import user as schemas
from ..services.user_service import UserService, get_user_service
from ..utils import create_access_token

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(tags=["authentication"])

@router.post(
    "/login",
    summary="Аутентификация",
    description="Аутентификация пользователя и получение JWT токена"
)
def login(
    form_data: schemas.UserLogin,
    user_service: UserService = Depends(get_user_service)
):
    user = user_service.authenticate_user(form_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email or password are incorrect",
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "user": user
    }