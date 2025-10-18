from sqlalchemy.orm import Session
from typing import Optional
from fastapi import Depends, HTTPException, status

from ..database import get_db
from ..crud.user import user_repository as user_repo
from ..schemas import user as schemas
from ..utils import get_password_hash, verify_password


class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: schemas.UserCreate) -> schemas.UserResponse:
        try:
            current_email = user_data.email
            if user_repo.get_by_email(self.db, current_email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This email already taken"
                )
            user_data.password = get_password_hash(user_data.password)
            db_user = user_repo.create(self.db, user_data)
            return schemas.UserResponse.model_validate(db_user)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    def get_user(self, user_id: int) -> schemas.UserResponse:
        """Получение пользователя"""
        db_user = user_repo.get_by_id(self.db, user_id)
        
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The user not found"
            )
        return schemas.UserResponse.model_validate(db_user)
    
    def get_users(self, skip: int, limit: int) -> schemas.UserResponse:
        """Получение пользователя"""
        db_user = user_repo.get_all(self.db, skip,limit)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The user not found"
            )
        return [schemas.UserResponse.model_validate(user) for user in db_user]
    
    def update_user(self, user_id: int, user_data: schemas.UserUpdate) -> schemas.UserResponse:
        """Обновление пользователя"""
        if not user_repo.get_by_id(self.db, user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The user not found"
            )
        if user_data.password:
            user_data.password = get_password_hash(user_data.password)
        if user_data.email:
            other_user = user_repo.get_by_email(self.db, user_data.email)
            if other_user and other_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This email already taken"
                )
        db_user = user_repo.update(self.db, user_id, user_data)
        return schemas.UserResponse.model_validate(db_user)
    
    def authenticate_user(self, user_data: schemas.UserLogin) -> Optional[schemas.UserResponse]:
        db_user = user_repo.get_by_email(self.db, user_data.email)
        if not db_user or not verify_password(user_data.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Login or password are incorrect"
            )
        return schemas.UserResponse.model_validate(db_user)    


def get_user_service(db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service