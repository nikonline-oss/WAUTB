from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..crud.user import user
from ..database import get_db


router = APIRouter()

@router.post("/create")
def create_user(data_user: dict, db: Session = Depends(get_db)):
    object = user.create(db, data_user)
    return {"object": object}

# @router.post("/login")
# def login_user():
#     ...

# @router.get("/me")
# def get_user():
#     ...

# def update_user():
#     ...

# def delete_user():
#     ...
