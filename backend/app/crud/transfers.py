from __future__ import annotations
from sqlalchemy.orm import Session
from .. import models
from ..schemas import transfers as schemas

def get_transfer(db: Session, id: int):
    return db.query(models.Transfer).get(id)

def get_transfers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Transfer).offset(skip).limit(limit).all()

def create_transfer(db: Session, obj_in: schemas.TransferCreate):
    transfer = models.Transfer(
        organization_id=obj_in.organization_id,
        date_of_issue=obj_in.date_of_issue,
    )
    db.add(transfer)
    db.flush()  # чтобы получить transfer.id до commit

    # добавляем позиции
    for item in obj_in.items:
        db.add(models.TransferItem(
            transfer_id=transfer.id,
            employee_id=item.employee_id,
            tabel_num=item.tabel_num,
            structure_id_before=item.structure_id_before,
            structure_id_after=item.structure_id_after,
            position_id_before=item.position_id_before,
            position_id_after=item.position_id_after,
            tarif=item.tarif,
            date_from=item.date_from,
            date_to=item.date_to,
            base_num=item.base_num,
            base_date=item.base_date
        ))

    db.commit()
    db.refresh(transfer)
    return transfer

def update_transfer(db: Session, db_obj: models.Transfer, obj_in: schemas.TransferUpdate):
    # обновляем шапку
    db_obj.organization_id = obj_in.organization_id
    db_obj.date_of_issue = obj_in.date_of_issue

    # заменяем состав позиций
    db.query(models.TransferItem).filter(models.TransferItem.transfer_id == db_obj.id).delete()
    db.flush()

    for item in obj_in.items:
        db.add(models.TransferItem(
            transfer_id=db_obj.id,
            employee_id=item.employee_id,
            tabel_num=item.tabel_num,
            structure_id_before=item.structure_id_before,
            structure_id_after=item.structure_id_after,
            position_id_before=item.position_id_before,
            position_id_after=item.position_id_after,
            tarif=item.tarif,
            date_from=item.date_from,
            date_to=item.date_to,
            base_num=item.base_num,
            base_date=item.base_date
        ))

    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_transfer(db: Session, db_obj: models.Transfer):
    db.delete(db_obj)
    db.commit()