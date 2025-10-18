# services/table_service.py
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from ..database import get_db
from ..crud.table import table_template_repository, table_column_repository, table_record_repository
from ..schemas import table as schemas
from fastapi import Depends, HTTPException, status

class TableTemplateService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_template(self, template_data: schemas.TableTemplateCreate) -> schemas.TableTemplateResponse:
        db_template = table_template_repository.create(self.db, template_data)
        return schemas.TableTemplateResponse.model_validate(db_template)
    
    def create_template_with_columns(self, template_data: schemas.TableTemplateCreateWithColumns) -> schemas.TableTemplateResponse:
        db_template = table_template_repository.create_with_columns(self.db, template_data)
        return schemas.TableTemplateResponse.model_validate(db_template)

    def get_template(self, template_id: int) -> schemas.TableTemplateResponse:
        db_template = table_template_repository.get_by_id(self.db, template_id)
        if not db_template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Шаблон таблицы не найден"
            )
        return schemas.TableTemplateResponse.model_validate(db_template)
    
    def get_templates(self, skip: int = 0, limit: int = 100) -> List[schemas.TableTemplateResponse]:
        db_templates = table_template_repository.get_all(self.db, skip, limit)
        return [schemas.TableTemplateResponse.model_validate(template) for template in db_templates]
    
    def update_template(self, template_id: int, template_data: schemas.TableTemplateUpdate) -> schemas.TableTemplateResponse:
        db_template = table_template_repository.update(self.db, template_id, template_data)
        if not db_template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Шаблон таблицы не найден"
            )
        return schemas.TableTemplateResponse.model_validate(db_template)
    
    def delete_template(self, template_id: int) -> bool:
        return table_template_repository.delete(self.db, template_id)

class TableColumnService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_column(self, column_data: schemas.TableColumnCreate) -> schemas.TableColumnResponse:
        db_column = table_column_repository.create(self.db, column_data)
        return schemas.TableColumnResponse.model_validate(db_column)
    
    def get_columns_by_template(self, template_id: int) -> List[schemas.TableColumnResponse]:
        db_columns = table_column_repository.get_by_template_id(self.db, template_id)
        return [schemas.TableColumnResponse.model_validate(column) for column in db_columns]
    
    def update_column(self, column_id: int, column_data: schemas.TableColumnUpdate) -> schemas.TableColumnResponse:
        db_column = table_column_repository.update(self.db, column_id, column_data)
        if not db_column:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Колонка не найдена"
            )
        return schemas.TableColumnResponse.model_validate(db_column)
    
    def delete_column(self, column_id: int) -> bool:
        return table_column_repository.delete(self.db, column_id)

class TableRecordService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_record(self, record_data: schemas.TableRecordCreate) -> schemas.TableRecordResponse:
        db_record = table_record_repository.create(self.db, record_data)
        return schemas.TableRecordResponse.model_validate(db_record)
    
    def get_records_by_template(self, template_id: int, skip: int = 0, limit: int = 100) -> List[schemas.TableRecordResponse]:
        db_records = table_record_repository.get_by_template_id(self.db, template_id, skip, limit)
        return [schemas.TableRecordResponse.model_validate(record) for record in db_records]
    
    def update_record(self, record_id: int, record_data: schemas.TableRecordUpdate) -> schemas.TableRecordResponse:
        db_record = table_record_repository.update(self.db, record_id, record_data)
        if not db_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Запись не найдена"
            )
        return schemas.TableRecordResponse.model_validate(db_record)
    
    def delete_record(self, record_id: int) -> bool:
        return table_record_repository.delete(self.db, record_id)

# Фабрики для dependency injection
def get_table_template_service(db: Session = Depends(get_db)):
    return TableTemplateService(db)

def get_table_column_service(db: Session = Depends(get_db)):
    return TableColumnService(db)

def get_table_record_service(db: Session = Depends(get_db)):
    return TableRecordService(db)
