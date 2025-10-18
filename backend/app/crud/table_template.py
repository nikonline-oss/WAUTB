# crud/table_template.py
from sqlalchemy.orm import Session, joinedload
from typing import List , Optional , Dict
from .base import CRUDBase
from models import TableTemplate, TableColumn
from ..schemas.TableTemplate import TableTemplateCreate, TableTemplateUpdate

class CRUDTableTemplate(CRUDBase):
    def __init__(self):
        super().__init__(TableTemplate)

    def get_with_columns(self, db: Session, id: int) -> Optional[TableTemplate]:
        return db.query(TableTemplate)\
            .options(joinedload(TableTemplate.columns))\
            .filter(TableTemplate.id == id)\
            .first()

    def get_multi_with_columns(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[TableTemplate]:
        return db.query(TableTemplate)\
            .options(joinedload(TableTemplate.columns))\
            .offset(skip)\
            .limit(limit)\
            .all()

    def create_with_columns(self, db: Session, *, template_data: Dict, columns: List[Dict]) -> TableTemplate:
        # Создаем шаблон таблицы
        db_template = TableTemplate(**template_data)
        db.add(db_template)
        db.flush()  # Получаем ID для связей

        # Создаем колонки
        for col_data in columns:
            col_data['table_template_id'] = db_template.id
            db_column = TableColumn(**col_data)
            db.add(db_column)

        db.commit()
        db.refresh(db_template)
        return db_template

    def update_with_columns(self, db: Session, *, template_id: int, template_data: Dict, columns: List[Dict]) -> TableTemplate:
        # Обновляем шаблон
        db_template = self.get(db, template_id)
        if not db_template:
            return None

        for field, value in template_data.items():
            if hasattr(db_template, field):
                setattr(db_template, field, value)

        # Удаляем старые колонки и добавляем новые
        db.query(TableColumn).filter(TableColumn.table_template_id == template_id).delete()
        
        for col_data in columns:
            col_data['table_template_id'] = template_id
            db_column = TableColumn(**col_data)
            db.add(db_column)

        db.commit()
        db.refresh(db_template)
        return db_template

table_template = CRUDTableTemplate()