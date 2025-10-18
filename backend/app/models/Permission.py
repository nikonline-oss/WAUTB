# models/role.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Table, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


# Связь многие-ко-многим для ролей и разрешений
role_permission = Table(
    'role_permission',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, nullable=False)  # Уникальный код права
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    category = Column(String(50))  # Группировка прав по категориям
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    roles = relationship("Role", secondary=role_permission, back_populates="permissions")
