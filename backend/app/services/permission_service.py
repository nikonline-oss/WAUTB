# services/permission_service.py
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from fastapi import Depends, HTTPException, status

from ..database import get_db
from ..crud.user import user_repository
from ..crud.table import table_template_repository
from ..crud.permission import user_table_permission_repository
from ..schemas import permission as schemas

class PermissionService:
    def __init__(self, db: Session):
        self.db = db
    
    def check_permission(self, user_id: int, table_template_id: int, permission_type: str) -> bool:
        """Проверка конкретного права пользователя на таблицу"""
        user = user_repository.get_by_id(self.db, user_id)
        if not user:
            return False
        
        # Администраторы имеют все права
        if user.role == 'admin':
            return True
        
        # Для сотрудников проверяем права в таблице разрешений
        permission = user_table_permission_repository.get_by_user_and_table(
            self.db, user_id, table_template_id
        )
        
        if not permission:
            return False
        
        # Проверяем конкретное право
        if permission_type == 'view':
            return permission.can_view
        elif permission_type == 'add_rows':
            return permission.can_add_rows
        elif permission_type == 'edit_rows':
            return permission.can_edit_rows
        elif permission_type == 'delete_rows':
            return permission.can_delete_rows
        elif permission_type == 'edit_structure':
            return permission.can_edit_structure
        elif permission_type == 'can_add_table':
            return permission.can_add_table
        
        return False
    
    def get_user_permissions(self, user_id: int) -> List[schemas.UserTablePermissionResponse]:
        """Получение всех прав пользователя"""
        permissions = user_table_permission_repository.get_by_user_id(self.db, user_id)
        return [schemas.UserTablePermissionResponse.model_validate(perm) for perm in permissions]
    
    def get_table_permissions(self, table_template_id: int) -> List[schemas.UserTablePermissionResponse]:
        """Получение всех прав на таблицу"""
        permissions = user_table_permission_repository.get_by_table_id(self.db, table_template_id)
        return [schemas.UserTablePermissionResponse.model_validate(perm) for perm in permissions]
    
    def set_user_permission(self, permission_data: schemas.UserTablePermissionCreate) -> schemas.UserTablePermissionResponse:
        """Установка права пользователя на таблицу"""
        # Проверяем существование пользователя и таблицы
        user = user_repository.get_by_id(self.db, permission_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        
        table = table_template_repository.get_by_id(self.db, permission_data.table_template_id)
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Таблица не найдена"
            )
        
        try:
            db_permission = user_table_permission_repository.create(self.db, permission_data)
            return schemas.UserTablePermissionResponse.model_validate(db_permission)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    def update_user_permission(self, permission_id: int, permission_data: schemas.UserTablePermissionUpdate) -> schemas.UserTablePermissionResponse:
        """Обновление права пользователя"""
        db_permission = user_table_permission_repository.update(self.db, permission_id, permission_data)
        if not db_permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Право не найдено"
            )
        return schemas.UserTablePermissionResponse.model_validate(db_permission)
    
    def bulk_update_permissions(self, bulk_data: schemas.BulkPermissionUpdate) -> List[schemas.UserTablePermissionResponse]:
        """Массовое обновление прав для пользователя на несколько таблиц"""
        user = user_repository.get_by_id(self.db, bulk_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        
        # Проверяем существование всех таблиц
        for table_id in bulk_data.table_template_ids:
            table = table_template_repository.get_by_id(self.db, table_id)
            if not table:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Таблица с ID {table_id} не найдена"
                )
        
        # Создаем словарь для массового обновления
        table_permissions = {}
        for table_id in bulk_data.table_template_ids:
            table_permissions[table_id] = bulk_data.permissions.model_dump(exclude_unset=True)
        
        # Устанавливаем права
        results = user_table_permission_repository.set_permissions_for_user_tables(
            self.db, bulk_data.user_id, table_permissions
        )
        
        return [schemas.UserTablePermissionResponse.model_validate(perm) for perm in results]
    
    def get_user_with_permissions(self, user_id: int) -> schemas.UserWithPermissions:
        """Получение пользователя со всеми его правами"""
        user = user_repository.get_by_id(self.db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        
        permissions = self.get_user_permissions(user_id)
        
        return schemas.UserWithPermissions(
            id=user.id,
            email=user.email,
            lastname=user.lastname,
            firstname=user.firstname,
            middlename=user.middlename,
            department_id=user.department_id,
            role=user.role,
            permissions=permissions
        )

# Фабрика для dependency injection
def get_permission_service(db: Session = Depends(get_db)):
    return PermissionService(db)