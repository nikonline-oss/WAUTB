from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routes import user_router, auth_router, department_router, table_router


app = FastAPI(title="Table Constructor API", version="1.0.0")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы, включая OPTIONS
    allow_headers=["*"],  # Разрешаем все заголовки
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(department_router)
app.include_router(table_router)

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