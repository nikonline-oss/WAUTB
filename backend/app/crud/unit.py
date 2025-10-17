from __future__ import annotations
from sqlalchemy.orm import Session
from .. import models
from ..schemas import units as schemas


def get_unit(db: Session, id: int):
    return db.query(models.Unit).get(id)

def get_units(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Unit).offset(skip).limit(limit).all()

def create_unit(db: Session, obj_in: schemas.UnitCreate):
    obj = models.Unit(**obj_in.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_unit(db: Session, db_obj: models.Unit, obj_in: schemas.UnitUpdate):
    for k, v in obj_in.model_dump().items():
        setattr(db_obj, k, v)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_unit(db: Session, db_obj: models.Unit):
    db.delete(db_obj)
    db.commit()