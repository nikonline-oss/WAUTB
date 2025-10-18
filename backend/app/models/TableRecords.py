# models.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

# 4. ДАННЫЕ ТАБЛИЦ
class TableRecord(Base):
    __tablename__ = "table_records"

    id = Column(Integer, primary_key=True, index=True)
    table_template_id = Column(Integer, ForeignKey("table_templates.id"), nullable=False)
    data = Column(JSON, nullable=False, default=dict)  # Основные данные в JSONB
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Связи
    table_template = relationship("TableTemplate", back_populates="records")
