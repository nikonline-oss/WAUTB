from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import User
from ..services.auth_service import get_password_hash, verify_password
from ..schemas.user import UserCreate, UserUpdate

class UserRepository:
    def init(self):
        pass
    
    # Только необходимые методы
    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()
    
    def create(self, db: Session, user_create: UserCreate) -> User:
        # Проверка уникальности email
        if self.get_by_email(db, user_create.email):
            raise ValueError("User with this email already exists")
        
        hashed_password = get_password_hash(user_create.password)
        
        db_user = User(
            email=user_create.email,
            password_hash=hashed_password,
            lastname=user_create.lastname,
            firstname=user_create.firstname,
            middlename=user_create.middlename,
            department=user_create.department
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def update(self, db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
        db_user = self.get_by_id(db, user_id)
        if not db_user:
            return None
        
        update_data = user_update.model_dump(exclude_unset=True)
        
        # Специфичная логика для пароля
        if "password" in update_data:
            update_data["password_hash"] = get_password_hash(update_data.pop("password"))
        
        # Специфичная логика для email
        if "email" in update_data:
            existing_user = self.get_by_email(db, update_data["email"])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already taken")
        
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def delete(self, db: Session, user_id: int) -> bool:
        db_user = self.get_by_id(db, user_id)
        if not db_user:
            return False
        
        db.delete(db_user)
        db.commit()
        return True
    
    # СПЕЦИФИЧНЫЕ методы для User
    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user
    
    def change_password(self, db: Session, user_id: int, new_password: str) -> bool:
        user = self.get_by_id(db, user_id)
        if not user:
            return False
        
        user.password_hash = get_password_hash(new_password)
        db.commit()
        return True
    
    def search_users(self, db: Session, query: str, department: Optional[str] = None) -> List[User]:
        search_filters = or_(
            User.email.ilike(f"%{query}%"),
            User.lastname.ilike(f"%{query}%"),
            User.firstname.ilike(f"%{query}%")
        )
        
        db_query = db.query(User).filter(search_filters)
        
        if department:
            db_query = db_query.filter(User.department == department)
        
        return db_query.all()

# Создаем экземпляр
user_repository = UserRepository()