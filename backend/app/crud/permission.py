# crud/permission.py
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..models import User, Roles
from ..schemas.permission import UserTablePermissionCreate, UserTablePermissionUpdate

class UserTablePermissionRepository:
    def get_by_id(self, db: Session, permission_id: int) -> Optional[Roles.UserTablePermission]:
        return db.query(Roles.UserTablePermission).filter(Roles.UserTablePermission.id == permission_id).first()
    
    def get_by_user_and_table(self, db: Session, user_id: int, table_template_id: int) -> Optional[Roles.UserTablePermission]:
        return db.query(Roles.UserTablePermission).filter(
            Roles.UserTablePermission.user_id == user_id,
            Roles.UserTablePermission.table_template_id == table_template_id
        ).first()
    
    def get_by_user_id(self, db: Session, user_id: int) -> List[Roles.UserTablePermission]:
        return db.query(Roles.UserTablePermission).filter(Roles.UserTablePermission.user_id == user_id).all()
    
    def get_by_table_id(self, db: Session, table_template_id: int) -> List[Roles.UserTablePermission]:
        return db.query(Roles.UserTablePermission).filter(Roles.UserTablePermission.table_template_id == table_template_id).all()
    
    def create(self, db: Session, permission_create: UserTablePermissionCreate) -> Roles.UserTablePermission:
        existing = self.get_by_user_and_table(db, permission_create.user_id, permission_create.table_template_id)
        if existing:
            raise ValueError("Permission for this user and table already exists")
        
        db_permission = Roles.UserTablePermission(**permission_create.model_dump())
        db.add(db_permission)
        db.commit()
        db.refresh(db_permission)
        return db_permission
    
    def update(self, db: Session, permission_id: int, permission_update: UserTablePermissionUpdate) -> Optional[Roles.UserTablePermission]:
        db_permission = self.get_by_id(db, permission_id)
        if not db_permission:
            return None
        
        update_data = permission_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_permission, field, value)
        
        db.commit()
        db.refresh(db_permission)
        return db_permission
    
    def update_by_user_and_table(self, db: Session, user_id: int, table_template_id: int, permission_update: UserTablePermissionUpdate) -> Optional[Roles.UserTablePermission]:
        db_permission = self.get_by_user_and_table(db, user_id, table_template_id)
        if not db_permission:
            return None
        
        update_data = permission_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_permission, field, value)
        
        db.commit()
        db.refresh(db_permission)
        return db_permission
    
    def delete(self, db: Session, permission_id: int) -> bool:
        db_permission = self.get_by_id(db, permission_id)
        if not db_permission:
            return False
        
        db.delete(db_permission)
        db.commit()
        return True
    
    def delete_by_user_and_table(self, db: Session, user_id: int, table_template_id: int) -> bool:
        db_permission = self.get_by_user_and_table(db, user_id, table_template_id)
        if not db_permission:
            return False
        
        db.delete(db_permission)
        db.commit()
        return True
    
    def set_permissions_for_user_tables(self, db: Session, user_id: int, table_permissions: Dict[int, Dict[str, bool]]) -> List[Roles.UserTablePermission]:
        """Массовое установление прав для пользователя на несколько таблиц"""
        results = []
        
        for table_template_id, permissions in table_permissions.items():
            # Проверяем существующую запись
            existing = self.get_by_user_and_table(db, user_id, table_template_id)
            
            if existing:
                # Обновляем существующую запись
                update_data = Roles.UserTablePermissionUpdate(**permissions)
                updated = self.update(existing.id, update_data)
                if updated:
                    results.append(updated)
            else:
                # Создаем новую запись
                permission_data = {
                    "user_id": user_id,
                    "table_template_id": table_template_id,
                    **permissions
                }
                new_permission = Roles.UserTablePermissionCreate(**permission_data)
                created = self.create(db, new_permission)
                if created:
                    results.append(created)
        
        return results

# Создаем экземпляр репозитория
user_table_permission_repository = UserTablePermissionRepository()