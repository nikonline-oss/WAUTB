from __future__ import annotations
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from .database import init_db


app = FastAPI(title="Доверенности (FastAPI)")

@app.on_event("startup")
async def on_startup():
    init_db()
