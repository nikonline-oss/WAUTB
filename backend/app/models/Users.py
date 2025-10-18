from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

# Связь многие-ко-многим для пользователей и таблиц с разрешениями
user_table_permission = Table(
    'user_table_permission',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('table_template_id', Integer, ForeignKey('table_templates.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    lastname = Column(String(100), nullable=False)
    firstname = Column(String(100), nullable=False)
    middlename = Column(String(100), nullable=False, default="")

    # role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, default=2)  # 2 - сотрудник по умолчанию
    
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    department = relationship("Department", back_populates="users")
    # role = relationship("Role", back_populates="users")
    table_permissions = relationship("Permission", secondary=user_table_permission)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
