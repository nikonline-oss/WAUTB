# app/websockets/table_sync_manager.py
from fastapi import WebSocket
from typing import Dict, Set, List, Optional
import json
from datetime import datetime
import logging
import asyncio

logger = logging.getLogger(__name__)

class TableSyncManager:
    """
    Специализированный менеджер для синхронизации таблиц
    """
    
    def __init__(self):
        # {user_id: WebSocket} - активные соединения
        self.active_connections: Dict[str, WebSocket] = {}
        
        # {table_id: Set[user_id]} - кто на какой таблице
        self.table_subscriptions: Dict[str, Set[str]] = {}
        
        # {table_id: {cell: user_id}} - блокировки ячеек
        self.cell_locks: Dict[str, Dict[str, str]] = {}
        
        # {table_id: {user_id: cursor_data}} - позиции курсоров
        self.user_cursors: Dict[str, Dict[str, dict]] = {}

    async def connect_to_table(self, websocket: WebSocket, user_id: str, table_id: str):
        """Подключиться к конкретной таблице"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        
        # Подписываем на таблицу
        if table_id not in self.table_subscriptions:
            self.table_subscriptions[table_id] = set()
            self.cell_locks[table_id] = {}
            self.user_cursors[table_id] = {}
            
        self.table_subscriptions[table_id].add(user_id)
        
        logger.info(f"User {user_id} connected to table {table_id}")
        
        # Уведомляем всех о новом пользователе
        await self._broadcast_to_table(table_id, {
            "type": "user_joined",
            "user_id": user_id,
            "table_id": table_id,
            "timestamp": datetime.now().isoformat(),
            "active_users": list(self.table_subscriptions[table_id])
        }, exclude_user=user_id)
        
        # Отправляем текущее состояние новому пользователю
        await self._send_to_user(user_id, {
            "type": "table_state",
            "table_id": table_id,
            "active_users": list(self.table_subscriptions[table_id]),
            "locked_cells": self.cell_locks[table_id],
            "user_cursors": self.user_cursors[table_id]
        })

    def disconnect(self, user_id: str):
        """Отключиться от всех таблиц"""
        if user_id not in self.active_connections:
            return
            
        # Удаляем из всех таблиц
        tables_to_cleanup = []
        for table_id, users in self.table_subscriptions.items():
            if user_id in users:
                users.remove(user_id)
                tables_to_cleanup.append(table_id)
                
                # Освобождаем заблокированные ячейки
                cells_to_unlock = []
                for cell, locked_by in self.cell_locks.get(table_id, {}).items():
                    if locked_by == user_id:
                        cells_to_unlock.append(cell)
                
                for cell in cells_to_unlock:
                    del self.cell_locks[table_id][cell]
                
                # Удаляем курсор
                if table_id in self.user_cursors and user_id in self.user_cursors[table_id]:
                    del self.user_cursors[table_id][user_id]
        
        # Удаляем соединение
        del self.active_connections[user_id]
        
        # Уведомляем об отключении (асинхронно)
        for table_id in tables_to_cleanup:
            asyncio.create_task(self._notify_user_left(table_id, user_id))
        
        logger.info(f"User {user_id} disconnected")

    async def _notify_user_left(self, table_id: str, user_id: str):
        """Уведомить о выходе пользователя"""
        await self._broadcast_to_table(table_id, {
            "type": "user_left",
            "user_id": user_id,
            "table_id": table_id,
            "timestamp": datetime.now().isoformat(),
            "active_users": list(self.table_subscriptions.get(table_id, []))
        })

    # 🎯 ОСНОВНЫЕ ФУНКЦИИ ДЛЯ СИНХРОНИЗАЦИИ ТАБЛИЦ

    async def sync_cell_update(self, table_id: str, user_id: str, cell_data: dict) -> bool:
        """
        Синхронизировать обновление ячейки
        """
        # Проверяем, что пользователь подключен к таблице
        if not self._is_user_subscribed(table_id, user_id):
            return False
            
        # Проверяем, что ячейка не заблокирована другим пользователем
        if not self._is_cell_editable(table_id, cell_data["cell"], user_id):
            await self._send_to_user(user_id, {
                "type": "cell_lock_error",
                "cell": cell_data["cell"],
                "message": "Ячейка заблокирована другим пользователем"
            })
            return False
        
        # Рассылаем обновление всем подписчикам таблицы
        await self._broadcast_to_table(table_id, {
            "type": "cell_updated",
            "table_id": table_id,
            "cell": cell_data["cell"],
            "value": cell_data["value"],
            "formula": cell_data.get("formula"),
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"Cell {cell_data['cell']} updated by {user_id} in table {table_id}")
        return True

    async def sync_cell_lock(self, table_id: str, user_id: str, cell: str, lock: bool) -> bool:
        """Заблокировать/разблокировать ячейку для редактирования"""
        if not self._is_user_subscribed(table_id, user_id):
            return False
            
        if lock:
            # Пытаемся заблокировать
            if self._is_cell_editable(table_id, cell, user_id):
                self.cell_locks[table_id][cell] = user_id
                await self._broadcast_to_table(table_id, {
                    "type": "cell_locked",
                    "table_id": table_id,
                    "cell": cell,
                    "user_id": user_id,
                    "timestamp": datetime.now().isoformat()
                })
                return True
            else:
                return False
        else:
            # Разблокировать
            if (table_id in self.cell_locks and 
                cell in self.cell_locks[table_id] and 
                self.cell_locks[table_id][cell] == user_id):
                
                del self.cell_locks[table_id][cell]
                await self._broadcast_to_table(table_id, {
                    "type": "cell_unlocked",
                    "table_id": table_id,
                    "cell": cell,
                    "user_id": user_id,
                    "timestamp": datetime.now().isoformat()
                })
                return True
        return False

    async def sync_cursor_move(self, table_id: str, user_id: str, cursor_data: dict):
        """Синхронизировать перемещение курсора"""
        if not self._is_user_subscribed(table_id, user_id):
            return
            
        self.user_cursors[table_id][user_id] = {
            **cursor_data,
            "last_updated": datetime.now().isoformat()
        }
        
        # Рассылаем обновление позиции курсора
        await self._broadcast_to_table(table_id, {
            "type": "cursor_moved",
            "table_id": table_id,
            "user_id": user_id,
            "cursor": cursor_data,
            "timestamp": datetime.now().isoformat()
        }, exclude_user=user_id)

    # 🛠️ ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ

    def _is_user_subscribed(self, table_id: str, user_id: str) -> bool:
        """Подписан ли пользователь на таблицу?"""
        return (table_id in self.table_subscriptions and 
                user_id in self.table_subscriptions[table_id])

    def _is_cell_editable(self, table_id: str, cell: str, user_id: str) -> bool:
        """Можно ли редактировать ячейку?"""
        if table_id not in self.cell_locks:
            return True
            
        current_locker = self.cell_locks[table_id].get(cell)
        return current_locker is None or current_locker == user_id

    async def _broadcast_to_table(self, table_id: str, message: dict, exclude_user: Optional[str] = None):
        """Разослать сообщение всем подписчикам таблицы"""
        if table_id not in self.table_subscriptions:
            return
        
        disconnected_users = []
        
        for user_id in list(self.table_subscriptions[table_id]):  # копируем список
            if user_id == exclude_user:
                continue
                
            if user_id in self.active_connections:
                try:
                    await self.active_connections[user_id].send_json(message)
                except Exception as e:
                    logger.error(f"Error sending to {user_id}: {e}")
                    disconnected_users.append(user_id)
        
        # Чистим отключившихся
        for user_id in disconnected_users:
            self.disconnect(user_id)

    async def _send_to_user(self, user_id: str, message: dict):
        """Отправить сообщение конкретному пользователю"""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
            except Exception as e:
                logger.error(f"Error sending to {user_id}: {e}")
                self.disconnect(user_id)

    # 📊 МЕТОДЫ ДЛЯ МОНИТОРИНГА

    def get_table_stats(self, table_id: str) -> dict:
        """Статистика по таблице"""
        if table_id not in self.table_subscriptions:
            return {"error": "Table not found"}
            
        return {
            "table_id": table_id,
            "active_users": list(self.table_subscriptions[table_id]),
            "locked_cells": self.cell_locks.get(table_id, {}),
            "user_cursors": self.user_cursors.get(table_id, {}),
            "total_connections": len(self.active_connections)
        }

    def get_user_tables(self, user_id: str) -> List[str]:
        """На каких таблицах сидит пользователь"""
        return [
            table_id for table_id, users in self.table_subscriptions.items()
            if user_id in users
        ]

# Глобальный экземпляр
table_sync_manager = TableSyncManager()