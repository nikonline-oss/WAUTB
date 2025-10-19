from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from jose import JWTError, jwt
from ..database import get_db
from ..crud.user import user_repository as user_repo
from ..core.config import settings
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Пропускаем аутентификацию для публичных endpoints
        public_paths = ["/login", "/auth/register", "/docs", "/openapi.json", "/redoc"]
        if request.url.path in public_paths:
            return await call_next(request)

        # Проверяем аутентификацию
        authorization: str = request.headers.get("Authorization")
        if authorization is None or not authorization.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Необходим токен авторизации"}
            )
        
        token = authorization.split("Bearer ")[1]
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            if not user_id:
                raise Exception("user_id not found")
        except JWTError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Недействительный токен"}
            )

        # Получаем пользователя
        db: Session = next(get_db())
        user = user_repo.get_by_id(db, int(user_id))
        if not user:
            return JSONResponse(
                status_code=401,
                content={"detail": "Пользователь не найден"}
            )

        request.state.current_user = user
        response = await call_next(request)
        return response