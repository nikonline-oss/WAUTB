from __future__ import annotations
from sqlalchemy.orm import Session
from .. import models
from ..schemas import employees as schemas


def get_employee(db: Session, id: int):
    return db.query(models.Employee).get(id)

def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employee).offset(skip).limit(limit).all()

def create_employee(db: Session, obj_in: schemas.EmployeeCreate):
    obj = models.Employee(**obj_in.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_employee(db: Session, db_obj: models.Employee, obj_in: schemas.EmployeeUpdate):
    for k, v in obj_in.model_dump().items():
        setattr(db_obj, k, v)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_employee(db: Session, db_obj: models.Employee):
    db.delete(db_obj)
    db.commit()