# crud/table_record.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional
import json

from .base import CRUDBase
from models import TableRecord, TableColumn
from ..schemas.TableRecord import TableRecordCreate, TableRecordUpdate
from ..schemas.paginate import PaginatedRequest, PaginatedResponse

class CRUDTableRecord(CRUDBase[TableRecord, TableRecordCreate, TableRecordUpdate]):
    def get_by_template(
        self, db: Session, table_template_id: int, *, skip: int = 0, limit: int = 100
    ) -> List[TableRecord]:
        return (
            db.query(TableRecord)
            .filter(TableRecord.table_template_id == table_template_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_paginated(
        self, db: Session, table_template_id: int, request: PaginatedRequest
    ) -> PaginatedResponse:
        query = db.query(TableRecord).filter(TableRecord.table_template_id == table_template_id)

        # Apply filters
        query = self._apply_filters(query, request.filters)
        
        # Apply search
        if request.search:
            query = self._apply_search(query, request.search)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply sorting
        query = self._apply_sorting(query, request.sort)
        
        # Apply pagination
        items = query.offset((request.page - 1) * request.per_page).limit(request.per_page).all()
        
        total_pages = (total + request.per_page - 1) // request.per_page
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=request.page,
            per_page=request.per_page,
            total_pages=total_pages
        )

    def _apply_filters(self, query, filters):
        for filter_cond in filters:
            field = filter_cond.field
            operator = filter_cond.operator
            value = filter_cond.value
            
            # Handle JSON field filtering
            json_field = TableRecord.data[field]
            
            if operator == 'eq':
                query = query.filter(json_field.astext == str(value))
            elif operator == 'ne':
                query = query.filter(json_field.astext != str(value))
            elif operator == 'gt':
                query = query.filter(json_field.astext > str(value))
            elif operator == 'lt':
                query = query.filter(json_field.astext < str(value))
            elif operator == 'gte':
                query = query.filter(json_field.astext >= str(value))
            elif operator == 'lte':
                query = query.filter(json_field.astext <= str(value))
            elif operator == 'like':
                query = query.filter(json_field.astext.ilike(f"%{value}%"))
            elif operator == 'in':
                if isinstance(value, list):
                    query = query.filter(json_field.astext.in_([str(v) for v in value]))
            elif operator == 'contains':
                query = query.filter(json_field.contains(value))
        
        return query

    def _apply_search(self, query, search_text: str):
        search_conditions = []
        
        search_conditions.append(
            TableRecord.data.cast(str).ilike(f"%{search_text}%")
        )
        
        return query.filter(or_(*search_conditions))

    def _apply_sorting(self, query, sort_conditions):
        if not sort_conditions:
            return query.order_by(TableRecord.updated_at.desc())
        
        for sort_cond in sort_conditions:
            field = sort_cond.field
            direction = sort_cond.direction
            
            if hasattr(TableRecord, field):
                column = getattr(TableRecord, field)
            else:
                column = TableRecord.data[field].astext
            
            if direction == 'desc':
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column.asc())
        
        return query

    def create(self, db: Session, *, obj_in: TableRecordCreate) -> TableRecord:
        obj_in_data = obj_in.dict()
        db_obj = TableRecord(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

table_record = CRUDTableRecord(TableRecord)