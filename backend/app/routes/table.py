from fastapi import APIRouter, Depends, status, Query, Path
from typing import List

from ..schemas import table as schemas
from ..services.table_service import TableTemplateService, TableColumnService, TableRecordService, get_table_template_service, get_table_column_service, get_table_record_service

router = APIRouter(prefix="/tables", tags=["users"])

@router.post(
    "/", 
    response_model=schemas.TableTemplateResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Создать таблицу",
    description="Создание новую таблицу в системе"
)
def create_table_template(
    table_data: schemas.TableTemplateCreateWithColumns,
    table_service: TableTemplateService = Depends(get_table_template_service)
):
    return table_service.create_template_with_columns(table_data)

@router.get(
    "/{table_id}/template", 
    response_model=schemas.TableTemplateResponse,
    summary="Получить таблицу по ID",
    description="Получение информации о таблице по его идентификатору"
)
def get_table_template(
    table_id: int = Path(..., description="ID table", gt=0),
    table_service: TableTemplateService = Depends(get_table_template_service)
):
    return table_service.get_template(table_id)

@router.get(
    "/",
    response_model=List[schemas.TableTemplateResponse],
    summary="Список шаблонов таблиц",
    description="Получение списка шаблонов таблиц с пагинацией"
)
def get_table_templates(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    table_service: TableTemplateService = Depends(get_table_template_service),
):
    return table_service.get_templates(skip, limit)

@router.put(
    "/{table_id}/template", 
    response_model=schemas.TableTemplateResponse,
    summary="Обновить шаблон таблицы",
    description="Обновление информации о таблице"
)
def update_table_template(
    table_id: int = Path(..., description="ID шаблона таблицы", gt=0),
    table_data: schemas.TableTemplateUpdate = None,
    table_service: TableTemplateService = Depends(get_table_template_service)
):
    return table_service.update_template(table_id, table_data)


@router.post(
    "/{table_id}",
    response_model=schemas.TableRecordResponse
)
def add_record(
    table_id: int = Path(..., gt=0),
    record_data: schemas.TableRecordCreate = None,
    table_service: TableRecordService = Depends(get_table_record_service)
):
    return table_service.create_record(record_data)

@router.get(
    "/{table_id}",
    response_model=List[schemas.TableRecordResponse]
)
def get_records(
    table_id: int = Path(..., gt=0),
    table_service: TableRecordService = Depends(get_table_record_service)
):
    return table_service.get_records_by_template(table_id)
