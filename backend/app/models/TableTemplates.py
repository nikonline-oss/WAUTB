# models.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


# 2. ШАБЛОНЫ ТАБЛИЦ
class TableTemplate(Base):
    __tablename__ = "table_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Связи
    columns = relationship("TableColumn", back_populates="table_template", cascade="all, delete-orphan")
    records = relationship("TableRecord", back_populates="table_template")
