# app/websockets/__init__.py
from .connection_manager import manager

# Экспортируем manager для использования в других модулях
__all__ = ["manager"]