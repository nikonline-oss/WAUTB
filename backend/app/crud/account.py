from __future__ import annotations
from sqlalchemy.orm import Session
from .. import models
from ..schemas import accounts as schemas


def get_account(db: Session, id: int):
    return db.query(models.Account).get(id)

def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Account).offset(skip).limit(limit).all()

def create_account(db: Session, obj_in: schemas.AccountCreate):
    obj = models.Account(**obj_in.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_account(db: Session, db_obj: models.Account, obj_in: schemas.AccountUpdate):
    for k, v in obj_in.model_dump().items():
        setattr(db_obj, k, v)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_account(db: Session, db_obj: models.Account):
    db.delete(db_obj)
    db.commit()