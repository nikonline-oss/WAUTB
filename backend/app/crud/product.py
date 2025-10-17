from __future__ import annotations
from sqlalchemy.orm import Session
from .. import models
from ..schemas import products as schemas


def get_product(db: Session, id: int):
    return db.query(models.Product).get(id)

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, obj_in: schemas.ProductCreate):
    obj = models.Product(**obj_in.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_product(db: Session, db_obj: models.Product, obj_in: schemas.ProductUpdate):
    for k, v in obj_in.model_dump().items():
        setattr(db_obj, k, v)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_product(db: Session, db_obj: models.Product):
    db.delete(db_obj)
    db.commit()