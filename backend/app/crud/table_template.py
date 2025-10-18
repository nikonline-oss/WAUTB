# crud/table_template.py
from sqlalchemy.orm import Session, joinedload
from typing import List , Optional 
from .base import CRUDBase
from models import TableTemplate
from ..schemas.TableTemplate import TableTemplateCreate, TableTemplateUpdate

class CRUDTableTemplate(CRUDBase[TableTemplate, TableTemplateCreate, TableTemplateUpdate]):
    def get_with_columns(self, db: Session, id: int) -> Optional[TableTemplate]:
        return db.query(TableTemplate).options(joinedload(TableTemplate.columns)).filter(TableTemplate.id == id).first()

    def get_multi_with_columns(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[TableTemplate]:
        return db.query(TableTemplate).options(joinedload(TableTemplate.columns)).offset(skip).limit(limit).all()

table_template = CRUDTableTemplate(TableTemplate)