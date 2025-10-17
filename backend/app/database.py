from __future__ import annotations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .core.config import DATABASE_URL



engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

# Зависимость FastAPI для получения сессии в обработчиках
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Создание таблиц по моделям — будет вызвано при старте приложения
def init_db():
    from . import models
    Base.metadata.create_all(bind=engine)