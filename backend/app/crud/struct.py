from __future__ import annotations
from sqlalchemy.orm import Session
from .. import models
from ..schemas import struct as schemas

def get_structure(db: Session, id: int):
    return db.query(models.Structure).get(id)

def get_structures(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Structure).offset(skip).limit(limit).all()

def create_structure(db: Session, obj_in: schemas.StructureCreate):
    obj = models.Structure(**obj_in.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_structure(db: Session, db_obj: models.Structure, obj_in: schemas.StructureUpdate):
    for k, v in obj_in.model_dump().items():
        setattr(db_obj, k, v)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_structure(db: Session, db_obj: models.Structure):
    db.delete(db_obj)
    db.commit()