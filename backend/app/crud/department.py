from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from ..models import Department
from ..schemas.department import DepartmentCreate, DepartmentUpdate


class DepartmentRepository:
    def init(self):
        pass
    
    def get_by_id(self, db: Session, department_id: int) -> Optional[Department]:
        return db.query(Department).filter(Department.id == department_id).first()
    
    def get_by_id_with_users(self, db: Session, department_id: int) -> Optional[Department]:
        return db.query(Department).options(joinedload(Department.users)).filter(Department.id == department_id).first()
    
    def get_by_title(self, db: Session, title: str) -> Optional[Department]:
        return db.query(Department).filter(Department.title == title).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Department]:
        return db.query(Department).offset(skip).limit(limit).all()
    
    def create(self, db: Session, department_create: DepartmentCreate) -> Department:
        db_department = Department(
            title=department_create.title,
        )
        db.add(db_department)
        db.commit()
        db.refresh(db_department)
        return db_department
    
    def update(self, db: Session, department_id: int, department_update: DepartmentUpdate) -> Optional[Department]:
        db_department = self.get_by_id(db, department_id)        
        update_data = department_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_department, field, value)
        db.commit()
        db.refresh(db_department)
        return db_department
    
    def delete(self, db: Session, department_id: int) -> bool:
        db_department = self.get_by_id(db, department_id)
        if not db_department:
            return False
        
        db.delete(db_department)
        db.commit()
        return True

department_repository = DepartmentRepository()