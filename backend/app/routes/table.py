from fastapi import APIRouter, Depends, status, Query, Path
from typing import List

from ..schemas import table as schemas
from ..services.table_service import TableTemplateService, TableColumnService, TableRecordService, get_table_template_service, get_table_column_service, get_table_record_service

router = APIRouter(prefix="/tables", tags=["users"])

@router.post(
    "/", 
    response_model=schemas.UserResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Создать таблицу",
    description="Создание новую таблицу в системе"
)
def create_table_template(
    table_data: schemas.TableTemplateCreate,
    table_service: TableTemplateService = Depends(get_table_template_service)
):
    return table_service.create_template(table_data)

@router.get(
    "/me", 
    response_model=schemas.UserResponse,
    summary="Получить текущего пользователя",
    description="Получение информации о текущем аутентифицированном пользователе"
)
def get_current_user_info(
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    return current_user

@router.get(
    "/{user_id}", 
    response_model=schemas.UserResponse,
    summary="Получить пользователя по ID",
    description="Получение информации о пользователе по его идентификатору"
)
def get_user(
    user_id: int = Path(..., description="ID пользователя", gt=0),
    user_service: UserService = Depends(get_user_service)
):
    return user_service.get_user(user_id)

@router.get(
    "/",
    response_model=List[schemas.UserResponse],
    summary="Список пользователей",
    description="Получение списка пользователей с пагинацией"
)
def get_users(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    user_service: UserService = Depends(get_user_service),
):
    return user_service.get_users(skip, limit)

@router.put(
    "/{user_id}", 
    response_model=schemas.UserResponse,
    summary="Обновить пользователя",
    description="Обновление информации о пользователе"
)
def update_user(
    user_id: int = Path(..., description="ID пользователя", gt=0),
    user_data: schemas.UserUpdate = None,
    user_service: UserService = Depends(get_user_service)
):
    return user_service.update_user(user_id, user_data)
