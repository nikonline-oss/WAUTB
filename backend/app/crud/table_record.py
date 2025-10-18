# crud/table_record.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional,DI
import json

from .base import CRUDBase
from models import TableRecord, TableColumn
from ..schemas.TableRecord import TableRecordCreate, TableRecordUpdate
from ..schemas.paginate import PaginatedRequest, PaginatedResponse

class CRUDTableRecord(CRUDBase):
    def __init__(self):
        super().__init__(TableRecord)

    def _build_filters(self, query, filters: List[Dict]):
        """Строит фильтры для JSONB поля data"""
        if not filters:
            return query

        conditions = []
        for filter_item in filters:
            field = filter_item.get('field')
            operator = filter_item.get('operator', '=')
            value = filter_item.get('value')

            if not field:
                continue

            json_field = TableRecord.data[field]

            if operator == '=':
                conditions.append(json_field.astext == str(value))
            elif operator == '!=':
                conditions.append(json_field.astext != str(value))
            elif operator == '>':
                conditions.append(cast(json_field.astext, String) > str(value))
            elif operator == '<':
                conditions.append(cast(json_field.astext, String) < str(value))
            elif operator == '>=':
                conditions.append(cast(json_field.astext, String) >= str(value))
            elif operator == '<=':
                conditions.append(cast(json_field.astext, String) <= str(value))
            elif operator == 'contains':
                conditions.append(json_field.astext.ilike(f'%{value}%'))
            elif operator == 'in' and isinstance(value, list):
                conditions.append(json_field.astext.in_([str(v) for v in value]))
            elif operator == 'not_in' and isinstance(value, list):
                conditions.append(~json_field.astext.in_([str(v) for v in value]))

        if conditions:
            query = query.filter(and_(*conditions))
        
        return query

    def _build_search(self, query, search_text: str, searchable_columns: List[str] = None):
        """Глобальный поиск по всем текстовым полям"""
        if not search_text:
            return query

        search_conditions = []
        search_pattern = f'%{search_text}%'

        # Если указаны конкретные колонки для поиска
        if searchable_columns:
            for column in searchable_columns:
                search_conditions.append(TableRecord.data[column].astext.ilike(search_pattern))
        else:
            # Ищем по всем текстовым полям в JSONB
            search_conditions.append(cast(TableRecord.data, String).ilike(search_pattern))

        return query.filter(or_(*search_conditions))

    def _build_sort(self, query, sort_by: str, sort_order: str = 'asc'):
        """Сортировка по полям JSONB или стандартным полям"""
        if not sort_by:
            return query.order_by(TableRecord.id.desc())

        # Сортировка по стандартным полям
        if hasattr(TableRecord, sort_by):
            field = getattr(TableRecord, sort_by)
            if sort_order.lower() == 'desc':
                return query.order_by(desc(field))
            else:
                return query.order_by(asc(field))
        
        # Сортировка по JSONB полям
        json_field = TableRecord.data[sort_by]
        if sort_order.lower() == 'desc':
            return query.order_by(desc(cast(json_field.astext, String)))
        else:
            return query.order_by(asc(cast(json_field.astext, String)))

    def get_records_with_pagination(
        self, 
        db: Session, 
        table_template_id: int,
        *,
        page: int = 1,
        per_page: int = 50,
        search_text: str = None,
        filters: List[Dict] = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        include_template: bool = False
    ) -> Dict[str, Any]:
        """
        Сложная пагинация с фильтрацией, поиском и сортировкой
        Возвращает: {
            'records': List[TableRecord],
            'total': int,
            'page': int,
            'per_page': int,
            'total_pages': int
        }
        """
        # Базовый запрос
        query = db.query(TableRecord).filter(
            TableRecord.table_template_id == table_template_id
        )

        # Применяем поиск
        if search_text:
            query = self._build_search(query, search_text)

        # Применяем фильтры
        if filters:
            query = self._build_filters(query, filters)

        # Получаем общее количество для пагинации
        total = query.count()

        # Применяем сортировку
        query = self._build_sort(query, sort_by, sort_order)

        # Применяем пагинацию
        records = query.offset((page - 1) * per_page).limit(per_page).all()

        # Включаем информацию о шаблоне если нужно
        if include_template and records:
            template = db.query(TableTemplate).options(
                joinedload(TableTemplate.columns)
            ).filter(TableTemplate.id == table_template_id).first()
        else:
            template = None

        total_pages = math.ceil(total / per_page) if total > 0 else 1

        return {
            'records': records,
            'template': template,
            'pagination': {
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        }

    def create_bulk(self, db: Session, table_template_id: int, records_data: List[Dict]) -> List[TableRecord]:
        """Массовое создание записей"""
        records = []
        for record_data in records_data:
            db_record = TableRecord(
                table_template_id=table_template_id,
                data=record_data.get('data', {})
            )
            db.add(db_record)
            records.append(db_record)
        
        db.commit()
        for record in records:
            db.refresh(record)
        
        return records

    def update_data(self, db: Session, *, record_id: int, data: Dict) -> Optional[TableRecord]:
        """Обновляет только data поле записи"""
        record = self.get(db, record_id)
        if record:
            record.data = data
            db.commit()
            db.refresh(record)
        return record

    def get_by_data_field(self, db: Session, table_template_id: int, field: str, value: Any) -> List[TableRecord]:
        """Поиск записей по конкретному полю в data"""
        return db.query(TableRecord).filter(
            TableRecord.table_template_id == table_template_id,
            TableRecord.data[field].astext == str(value)
        ).all()

table_record = CRUDTableRecord()