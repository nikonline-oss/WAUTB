# models.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


# 3. КОЛОНКИ ШАБЛОНОВ
class TableColumn(Base):
    __tablename__ = "table_columns"

    id = Column(Integer, primary_key=True, index=True)
    table_template_id = Column(Integer, ForeignKey("table_templates.id"), nullable=False)
    name = Column(String(255), nullable=False)
    data_type = Column(String(50), nullable=False)  # text, number, boolean, date, datetime, select

    order_index = Column(Integer, default=0)
    config = Column(JSON, default=dict)  # Конфигурация для разных типов данных
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    table_template = relationship("TableTemplate", back_populates="columns")

