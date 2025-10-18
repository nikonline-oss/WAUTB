from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from ..models import User
from ..schemas.user import UserCreate, UserUpdate


class UserRepository:
    def init(self):
        pass
    
    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).options(joinedload(User.department)).filter(User.id == user_id).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).options(joinedload(User.department)).filter(User.email == email).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).options(joinedload(User.department)).offset(skip).limit(limit).all()
    
    def create(self, db: Session, user_create: UserCreate) -> User:
        db_user = User(
            email=user_create.email,
            password=user_create.password,
            lastname=user_create.lastname,
            firstname=user_create.firstname,
            middlename=user_create.middlename,
            department_id=user_create.department_id
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def update(self, db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
        db_user = self.get_by_id(db, user_id)        
        update_data = user_update.model_dump(exclude_unset=True)
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

user_repository = UserRepository()