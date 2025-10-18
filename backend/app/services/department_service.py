from sqlalchemy.orm import Session
from typing import Optional
from fastapi import Depends, HTTPException, status

from ..database import get_db
from ..crud.department import department_repository as department_repo
from ..schemas import department as schemas
from ..utils import get_password_hash, verify_password


class DepartmentService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_department(self, department_data: schemas.DepartmentCreate) -> schemas.DepartmentResponse:
        try:
            if department_repo.get_by_title(self.db, department_data.title):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This department already exists"
                )
            db_department = department_repo.create(self.db, department_data)
            return schemas.DepartmentResponse.model_validate(db_department)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    def get_department(self, department_id: int) -> schemas.DepartmentResponse:
        db_department = department_repo.get_by_id(self.db, department_id)
        if not db_department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The department not found"
            )
        return schemas.DepartmentResponse.model_validate(db_department)
    
    def get_departments(self, skip: int, limit: int) -> schemas.DepartmentResponse:
        db_department = department_repo.get_all(self.db, skip,limit)
        if not db_department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The department not found"
            )
        return [schemas.DepartmentResponse.model_validate(department) for department in db_department]
    
    def update_department(self, department_id: int, department_data: schemas.DepartmentUpdate) -> schemas.DepartmentResponse:
        if not department_repo.get_by_id(self.db, department_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The department not found"
            )
        if department_data.title:
            other_department = department_repo.get_by_title(self.db, department_data.title)
            if other_department and other_department.id != department_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This department already exists"
                )
        db_department = department_repo.update(self.db, department_id, department_data)
        return schemas.DepartmentResponse.model_validate(db_department)


def get_department_service(db: Session = Depends(get_db)):
    department_service = DepartmentService(db)
    return department_service
