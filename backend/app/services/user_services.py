from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..crud.user import user_repository as user_repo
from ..schemas import user as schemas
from fastapi import Depends, HTTPException, status

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: schemas.UserCreate) -> schemas.UserResponse:
        """Создание пользователя с бизнес-логикой"""
        try:
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
                detail="Пользователь не найден"
            )
        return schemas.UserResponse.model_validate(db_user)
    
    def get_users(self, skip: int, limit: int) -> schemas.UserResponse:
        """Получение пользователя"""
        db_user = user_repo.get_all(self.db, skip,limit)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        return [schemas.UserResponse.model_validate(user) for user in db_user]
    
    def update_user(self, user_id: int, user_data: schemas.UserUpdate) -> schemas.UserResponse:
        """Обновление пользователя"""
        db_user = user_repo.update(self.db, user_id, user_data)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        return schemas.UserResponse.model_validate(db_user)
    
    def authenticate_user(self, email: str, password: str) -> Optional[schemas.UserResponse]:
        """Аутентификация пользователя"""
        db_user = user_repo.authenticate(self.db, email, password)
        if not db_user:
            return None
        return schemas.UserResponse.model_validate(db_user)
    
    def search_users(self, query: str, department: Optional[str] = None) -> List[schemas.UserResponse]:
        """Поиск пользователей"""
        db_users = user_repo.search_users(self.db, query, department)
        return [schemas.UserResponse.model_validate(user) for user in db_users]
    

# Фабрика для dependency injection
def get_user_service(db: Session = Depends(get_db)):
    print(db)
    user_service = UserService(db)
    return user_service