from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    title = Column(String(100), nullable=False, unique=True)
    
    users = relationship("User", back_populates="department")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
