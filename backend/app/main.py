from __future__ import annotations
from fastapi import FastAPI
from .database import init_db
from .routes import user_router, auth_router, department_router


app = FastAPI(title="Table Constructor API", version="1.0.0")
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(department_router)

# Инициализация БД при старте
@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {
        "message": "Table Constructor API is running!",
        "docs": "/docs",
        "test_endpoints": [
            "POST /test/setup-sample-data/ - создать тестовые данные",
            "DELETE /test/clear-all-data/ - очистить все данные",
            "GET /users/ - получить всех пользователей",
            "POST /table-templates/ - создать шаблон таблицы",
            "POST /table-records/paginated/ - пагинация с фильтрацией"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)