from __future__ import annotations
from sqlalchemy.orm import Session
from .. import models
from ..schemas import organizations as schemas


def get_organization(db: Session, id: int):
    return db.query(models.Organization).get(id)

def get_organizations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Organization).offset(skip).limit(limit).all()

def create_organization(db: Session, obj_in: schemas.OrganizationCreate):
    obj = models.Organization(**obj_in.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_organization(db: Session, db_obj: models.Organization, obj_in: schemas.OrganizationUpdate):
    for k, v in obj_in.model_dump().items():
        setattr(db_obj, k, v)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_organization(db: Session, db_obj: models.Organization):
    db.delete(db_obj)
    db.commit()