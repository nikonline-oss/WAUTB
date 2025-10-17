from __future__ import annotations
from sqlalchemy.orm import Session
from .. import models
from ..schemas import departments as schemas


def get_department(db: Session, id: int):
    return db.query(models.Department).get(id)

def get_departments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Department).offset(skip).limit(limit).all()

def create_department(db: Session, obj_in: schemas.DepartmentCreate):
    obj = models.Department(**obj_in.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_department(db: Session, db_obj: models.Department, obj_in: schemas.DepartmentUpdate):
    for k, v in obj_in.model_dump().items():
        setattr(db_obj, k, v)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_department(db: Session, db_obj: models.Department):
    db.delete(db_obj)
    db.commit()