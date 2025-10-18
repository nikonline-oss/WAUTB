from fastapi import APIRouter, Depends, status, Query, Path
from typing import List

from ..schemas import department as schemas
from ..services.department_service import DepartmentService, get_department_service

router = APIRouter(prefix="/departments", tags=["departments"])

@router.post(
    "/", 
    response_model=schemas.DepartmentResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Создать отдел",
    description="Создание нового отдела в системе"
)
def create_department(
    department_data: schemas.DepartmentCreate,
    department_service: DepartmentService = Depends(get_department_service)
):
    return department_service.create_department(department_data)

@router.get(
    "/{department_id}", 
    response_model=schemas.DepartmentResponse,
    summary="Получить отдел по ID",
    description="Получение информации об отделе по его идентификатору"
)
def get_department(
    department_id: int = Path(..., description="ID пользователя", gt=0),
    department_service: DepartmentService = Depends(get_department_service)
):
    return department_service.get_department(department_id)

@router.get(
    "/",
    response_model=List[schemas.DepartmentResponse],
    summary="Список пользователей",
    description="Получение списка пользователей с пагинацией"
)
def get_departments(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    department_service: DepartmentService = Depends(get_department_service),
):
    return department_service.get_departments(skip, limit)

@router.put(
    "/{department_id}", 
    response_model=schemas.DepartmentResponse,
    summary="Обновить пользователя",
    description="Обновление информации о пользователе"
)
def update_department(
    department_id: int = Path(..., description="ID пользователя", gt=0),
    department_data: schemas.DepartmentUpdate = None,
    department_service: DepartmentService = Depends(get_department_service)
):
    return department_service.update_department(department_id, department_data)
