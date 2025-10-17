from __future__ import annotations
from sqlalchemy.orm import Session
from .. import models
from ..schemas import positions as schemas


def get_position(db: Session, id: int):
    return db.query(models.Position).get(id)

def get_positions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Position).offset(skip).limit(limit).all()

def create_position(db: Session, obj_in: schemas.PositionCreate):
    obj = models.Position(**obj_in.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_position(db: Session, db_obj: models.Position, obj_in: schemas.PositionUpdate):
    for k, v in obj_in.model_dump().items():
        setattr(db_obj, k, v)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_position(db: Session, db_obj: models.Position):
    db.delete(db_obj)
    db.commit()