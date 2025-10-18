# crud/table_column.py
from sqlalchemy.orm import Session
from typing import List, Dict
from .base import CRUDBase
from models import TableColumn

class CRUDTableColumn(CRUDBase):
    def __init__(self):
        super().__init__(TableColumn)

    def get_by_template(self, db: Session, table_template_id: int) -> List[TableColumn]:
        return db.query(TableColumn)\
            .filter(TableColumn.table_template_id == table_template_id)\
            .order_by(TableColumn.order_index)\
            .all()

    def update_order(self, db: Session, table_template_id: int, new_order: List[Dict]) -> List[TableColumn]:
        """Обновляет порядок колонок"""
        columns = self.get_by_template(db, table_template_id)
        column_map = {col.id: col for col in columns}
        
        for order_data in new_order:
            column_id = order_data['column_id']
            new_index = order_data['order_index']
            if column_id in column_map:
                column_map[column_id].order_index = new_index
        
        db.commit()
        return self.get_by_template(db, table_template_id)

table_column = CRUDTableColumn()