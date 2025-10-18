# crud/table.py
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..models import TableTemplate, TableColumn, TableRecord
from ..schemas.table import TableTemplateCreate, TableTemplateUpdate, TableColumnCreate, TableColumnUpdate, TableRecordCreate, TableRecordUpdate

class TableTemplateRepository:
    def get_by_id(self, db: Session, template_id: int) -> Optional[TableTemplate]:
        return db.query(TableTemplate).filter(TableTemplate.id == template_id).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[TableTemplate]:
        return db.query(TableTemplate).offset(skip).limit(limit).all()
    
    def create(self, db: Session, template_create: TableTemplateCreate) -> TableTemplate:
        db_template = TableTemplate(name=template_create.name)
        db.add(db_template)
        db.commit()
        db.refresh(db_template)
        return db_template
    
    def update(self, db: Session, template_id: int, template_update: TableTemplateUpdate) -> Optional[TableTemplate]:
        db_template = self.get_by_id(db, template_id)
        if not db_template:
            return None
        
        update_data = template_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_template, field, value)
        
        db.commit()
        db.refresh(db_template)
        return db_template
    
    def delete(self, db: Session, template_id: int) -> bool:
        db_template = self.get_by_id(db, template_id)
        if not db_template:
            return False
        
        db.delete(db_template)
        db.commit()
        return True

class TableColumnRepository:
    def get_by_id(self, db: Session, column_id: int) -> Optional[TableColumn]:
        return db.query(TableColumn).filter(TableColumn.id == column_id).first()
    
    def get_by_template_id(self, db: Session, template_id: int) -> List[TableColumn]:
        return db.query(TableColumn).filter(TableColumn.table_template_id == template_id).all()
    
    def create(self, db: Session, column_create: TableColumnCreate) -> TableColumn:
        db_column = TableColumn(**column_create.model_dump())
        db.add(db_column)
        db.commit()
        db.refresh(db_column)
        return db_column
    
    def update(self, db: Session, column_id: int, column_update: TableColumnUpdate) -> Optional[TableColumn]:
        db_column = self.get_by_id(db, column_id)
        if not db_column:
            return None
        
        update_data = column_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_column, field, value)
        
        db.commit()
        db.refresh(db_column)
        return db_column
    
    def delete(self, db: Session, column_id: int) -> bool:
        db_column = self.get_by_id(db, column_id)
        if not db_column:
            return False
        
        db.delete(db_column)
        db.commit()
        return True

class TableRecordRepository:
    def get_by_id(self, db: Session, record_id: int) -> Optional[TableRecord]:
        return db.query(TableRecord).filter(TableRecord.id == record_id).first()
    
    def get_by_template_id(self, db: Session, template_id: int, skip: int = 0, limit: int = 100) -> List[TableRecord]:
        return db.query(TableRecord).filter(TableRecord.table_template_id == template_id).offset(skip).limit(limit).all()
    
    def create(self, db: Session, record_create: TableRecordCreate) -> TableRecord:
        db_record = TableRecord(**record_create.model_dump())
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record
    
    def update(self, db: Session, record_id: int, record_update: TableRecordUpdate) -> Optional[TableRecord]:
        db_record = self.get_by_id(db, record_id)
        if not db_record:
            return None
        
        update_data = record_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_record, field, value)
        
        db.commit()
        db.refresh(db_record)
        return db_record
    
    def delete(self, db: Session, record_id: int) -> bool:
        db_record = self.get_by_id(db, record_id)
        if not db_record:
            return False
        
        db.delete(db_record)
        db.commit()
        return True

# Создаем экземпляры репозиториев
table_template_repository = TableTemplateRepository()
table_column_repository = TableColumnRepository()
table_record_repository = TableRecordRepository()