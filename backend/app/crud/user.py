from sqlalchemy.orm import Session
from typing import Optional, Dict
from .base import CRUDBase
from ..models import User
from ..services.auth_service import get_password_hash, verify_password



class CRUDUser(CRUDBase):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, obj_in: Dict) -> User:
        # Хешируем пароль перед сохранением
        print(obj_in["password"])
        obj_in['password_hash'] = get_password_hash(obj_in.pop('password'))
        return super().create(db, obj_in=obj_in)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

user = CRUDUser()