from __future__ import annotations
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from .database import init_db

app = FastAPI(title="Table Constructor API", version="1.0.0")

# Инициализация БД при старте
@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Table Constructor API is running!"}
