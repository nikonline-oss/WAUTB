from __future__ import annotations
from sqlalchemy.orm import Session
from .. import models
from ..schemas import proxies as schemas


def get_proxy(db: Session, id: int):
    return db.query(models.Proxy).get(id)

def get_proxies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Proxy).offset(skip).limit(limit).all()

def create_proxy(db: Session, obj_in: schemas.ProxyCreate):
    proxy = models.Proxy(
        organization_id=obj_in.organization_id,
        employee_id=obj_in.employee_id,
        customer_id=obj_in.customer_id,
        date_of_issue=obj_in.date_of_issue,
        is_valid_until=obj_in.is_valid_until,
    )
    db.add(proxy)
    db.flush()  # чтобы получить proxy.id до commit

    # добавляем позиции
    for item in obj_in.items:
        db.add(models.ProxyItem(
            proxy_id=proxy.id,
            product_id=item.product_id,
            amount=item.amount
        ))

    db.commit()
    db.refresh(proxy)
    return proxy

def update_proxy(db: Session, db_obj: models.Proxy, obj_in: schemas.ProxyUpdate):
    # обновляем шапку
    db_obj.organization_id = obj_in.organization_id
    db_obj.employee_id = obj_in.employee_id
    db_obj.customer_id = obj_in.customer_id
    db_obj.date_of_issue = obj_in.date_of_issue
    db_obj.is_valid_until = obj_in.is_valid_until

    # заменяем состав позиций (как в джанго-подходе "пересобрать")
    db.query(models.ProxyItem).filter(models.ProxyItem.proxy_id == db_obj.id).delete()
    db.flush()

    for item in obj_in.items:
        db.add(models.ProxyItem(
            proxy_id=db_obj.id,
            product_id=item.product_id,
            amount=item.amount
        ))

    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_proxy(db: Session, db_obj: models.Proxy):
    db.delete(db_obj)
    db.commit()