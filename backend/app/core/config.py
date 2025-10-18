# from __future__ import annotations
# import os
# from typing import Literal


# DATABASE_URL: str = os.getenv(
#     "DATABASE_URL",
#     "postgresql+psycopg://postgres:Post0Nik1line@localhost:5432/table_constructor"
# )

# config.py
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Excel Data Hub"
    PROJECT_VERSION: str = "1.0.0"
    
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "PostN0ik1line")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "table_constructor")
    
    # Кодируем пароль для URL
    ENCODED_PASSWORD = quote_plus(POSTGRES_PASSWORD)
    DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{ENCODED_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    # DATABASE_URL = "sqlite:///./test.db"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

settings = Settings()