from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from typing import List

from ..schemas import table as schemas
from ..services.table_service import TableTemplateService, TableColumnService, TableRecordService, get_table_template_service, get_table_column_service, get_table_record_service
from ..dependencies import check_edit_structure_permission, get_admin_user, check_view_permission, get_current_user, check_add_rows_permission, check_edit_rows_permission,check_delete_rows_permission

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
    table_service: TableTemplateService = Depends(get_table_template_service),
    current_user = Depends(get_admin_user) 
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
    table_service: TableTemplateService = Depends(get_table_template_service),
    current_user = Depends(get_current_user),
    _ = Depends(lambda: check_view_permission( Path(..., description="ID таблицы", gt=0))) 
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
    table_service: TableTemplateService = Depends(get_table_template_service),
    _ = Depends(lambda: check_edit_structure_permission( Path(..., description="ID таблицы", gt=0))) 
):
    return table_service.update_template(table_id, table_data)

@router.delete(
    "/{table_id}/template",
    status_code=status.HTTP_200_OK,
    summary="Удалить шаблон таблицы",
    description="Удаление шаблона таблицы и всех связанных данных"
)
def delete_table_template(
    table_id: int = Path(..., description="ID шаблона таблицы", gt=0),
    table_service: TableTemplateService = Depends(get_table_template_service),
    _ = Depends(lambda: check_edit_structure_permission( Path(..., description="ID таблицы", gt=0))) 
):
    success = table_service.delete_template(table_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Шаблон таблицы не найден"
        )
    return {"message": "Шаблон таблицы успешно удален"}

# TableColumn endpoints
@router.post(
    "/{table_id}/columns",
    response_model=schemas.TableColumnResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить колонку в таблицу",
    description="Добавление новой колонки в шаблон таблицы"
)
def create_table_column(
    table_id: int = Path(..., description="ID таблицы", gt=0),
    column_data: schemas.TableColumnCreate = None,
    column_service: TableColumnService = Depends(get_table_column_service),
    _ = Depends(lambda: check_edit_structure_permission( Path(..., description="ID таблицы", gt=0))) 
):
    # Устанавливаем table_template_id из пути
    column_data.table_template_id = table_id
    return column_service.create_column(column_data)

@router.get(
    "/{table_id}/columns",
    response_model=List[schemas.TableColumnResponse],
    summary="Получить колонки таблицы",
    description="Получение списка всех колонок таблицы"
)
def get_table_columns(
    table_id: int = Path(..., description="ID таблицы", gt=0),
    column_service: TableColumnService = Depends(get_table_column_service),
    _ = Depends(lambda: check_view_permission( Path(..., description="ID таблицы", gt=0))) 
):
    return column_service.get_columns_by_template(table_id)

@router.put(
    "/columns/{column_id}",
    response_model=schemas.TableColumnResponse,
    summary="Обновить колонку",
    description="Обновление информации о колонке таблицы"
)
def update_table_column(
    column_id: int = Path(..., description="ID колонки", gt=0),
    column_data: schemas.TableColumnUpdate = None,
    column_service: TableColumnService = Depends(get_table_column_service),
    _ = Depends(lambda: check_edit_structure_permission( Path(..., description="ID таблицы", gt=0))) 
):
    return column_service.update_column(column_id, column_data)

@router.delete(
    "/columns/{column_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить колонку",
    description="Удаление колонки из шаблона таблицы"
)
def delete_table_column(
    column_id: int = Path(..., description="ID колонки", gt=0),
    column_service: TableColumnService = Depends(get_table_column_service),
    _ = Depends(lambda: check_edit_structure_permission( Path(..., description="ID таблицы", gt=0))) 
):
    success = column_service.delete_column(column_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Колонка не найдена"
        )
    return {"message": "Колонка успешно удалена"}


# TableRecord endpoints
@router.post(
    "/{table_id}/records",
    response_model=schemas.TableRecordResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить запись в таблицу",
    description="Добавление новой записи в таблицу"
)
def add_record(
    table_id: int = Path(..., description="ID таблицы", gt=0),
    record_data: schemas.TableRecordCreate = None,
    record_service: TableRecordService = Depends(get_table_record_service),
    _ = Depends(lambda: check_add_rows_permission( Path(..., description="ID таблицы", gt=0))) 
):
    # Устанавливаем table_template_id из пути
    record_data.table_template_id = table_id
    return record_service.create_record(record_data)

@router.get(
    "/{table_id}/records",
    response_model=List[schemas.TableRecordResponse],
    summary="Получить записи таблицы",
    description="Получение списка записей таблицы с пагинацией"
)
def get_records(
    table_id: int = Path(..., description="ID таблицы", gt=0),
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    record_service: TableRecordService = Depends(get_table_record_service),
    current_user = Depends(get_admin_user) 
):
    return record_service.get_records_by_template(table_id, skip, limit)

@router.get(
    "/{table_id}/records/{record_id}",
    response_model=schemas.TableRecordResponse,
    summary="Получить запись по ID",
    description="Получение конкретной записи таблицы по идентификатору"
)
def get_record(
    table_id: int = Path(..., description="ID таблицы", gt=0),
    record_id: int = Path(..., description="ID записи", gt=0),
    record_service: TableRecordService = Depends(get_table_record_service)
):
    print(record_id)
    record = record_service.get_record(record_id)
    if not record or record.table_template_id != table_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись не найдена"
        )
    return record

@router.put(
    "/{table_id}/records/{record_id}",
    response_model=schemas.TableRecordResponse,
    summary="Обновить запись",
    description="Обновление данных записи в таблице"
)
def update_record(
    table_id: int = Path(..., description="ID таблицы", gt=0),
    record_id: int = Path(..., description="ID записи", gt=0),
    record_data: schemas.TableRecordUpdate = None,
    record_service: TableRecordService = Depends(get_table_record_service),
    _ = Depends(lambda: check_edit_rows_permission( Path(..., description="ID таблицы", gt=0))) 
):
    # В сервисе нужно добавить метод update_record
    # Пока используем существующий, предполагая что record_id уникален
    record = record_service.update_record(record_id, record_data)
    if not record or record.table_template_id != table_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись не найдена"
        )
    return record

@router.delete(
    "/{table_id}/records/{record_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить запись",
    description="Удаление записи из таблицы"
)
def delete_record(
    table_id: int = Path(..., description="ID таблицы", gt=0),
    record_id: int = Path(..., description="ID записи", gt=0),
    record_service: TableRecordService = Depends(get_table_record_service),
    _ = Depends(lambda: check_delete_rows_permission( Path(..., description="ID таблицы", gt=0))) 
):
    # Проверяем существование записи и принадлежность к таблице
    record = record_service.get_record(record_id)
    if not record or record.table_template_id != table_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись не найдена"
        )
    
    success = record_service.delete_record(record_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись не найдена"
        )
    return {"message": "Запись успешно удалена"}
