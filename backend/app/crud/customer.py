from __future__ import annotations
from sqlalchemy.orm import Session
from .. import models
from ..schemas import customers as schemas


def get_customer(db: Session, id: int):
    return db.query(models.Customer).get(id)

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()

def create_customer(db: Session, obj_in: schemas.CustomerCreate):
    obj = models.Customer(**obj_in.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_customer(db: Session, db_obj: models.Customer, obj_in: schemas.CustomerUpdate):
    for k, v in obj_in.model_dump().items():
        setattr(db_obj, k, v)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_customer(db: Session, db_obj: models.Customer):
    db.delete(db_obj)
    db.commit()