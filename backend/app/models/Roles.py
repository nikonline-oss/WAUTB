# models.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

# Таблица для связи пользователей, таблиц и прав
class UserTablePermission(Base):
    __tablename__ = "user_table_permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    table_template_id = Column(Integer, ForeignKey("table_templates.id"), nullable=False)
    
    # Права
    can_view = Column(Boolean, default=False)           # Просмотр таблицы
    can_add_rows = Column(Boolean, default=False)       # Добавление строк
    can_edit_rows = Column(Boolean, default=False)      # Редактирование строк
    can_delete_rows = Column(Boolean, default=False)    # Удаление строк
    can_edit_structure = Column(Boolean, default=False) # Редактирование структуры таблицы
    can_add_table = Column(Boolean, default=False)      # Добавление таблиц

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Связи
    user = relationship("User", back_populates="table_permissions")
    table_template = relationship("TableTemplate", back_populates="user_permissions")
