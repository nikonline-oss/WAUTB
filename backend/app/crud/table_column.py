# crud/table_column.py
from sqlalchemy.orm import Session
from typing import List
from .base import CRUDBase
from models import TableColumn
from ..schemas.TableColumn import TableColumnCreate, TableColumnUpdate

class CRUDTableColumn(CRUDBase[TableColumn, TableColumnCreate, TableColumnUpdate]):
    def get_by_template(self, db: Session, table_template_id: int) -> List[TableColumn]:
        return db.query(TableColumn).filter(TableColumn.table_template_id == table_template_id).all()

    def create(self, db: Session, *, obj_in: TableColumnCreate) -> TableColumn:
        obj_in_data = obj_in.dict()
        db_obj = TableColumn(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

table_column = CRUDTableColumn(TableColumn)