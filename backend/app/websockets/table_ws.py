# app/websockets/table_ws.py
from fastapi import WebSocket, WebSocketDisconnect
from websockets.connection_manager import table_sync_manager
import logging

logger = logging.getLogger(__name__)

async def handle_table_websocket(websocket: WebSocket, table_id: str, user_id: str):
    """
    Обработчик WebSocket для конкретной таблицы
    """
    await table_sync_manager.connect_to_table(websocket, user_id, table_id)
    
    try:
        while True:
            # Ждём сообщения от клиента
            data = await websocket.receive_json()
            
            # 🎯 Обрабатываем ТОЛЬКО сообщения связанные с таблицами
            if data["type"] == "cell_update":
                await table_sync_manager.sync_cell_update(
                    table_id, user_id, data["cell_data"]
                )
                
            elif data["type"] == "cell_lock":
                success = await table_sync_manager.sync_cell_lock(
                    table_id, user_id, data["cell"], data["lock"]
                )
                # Отправляем результат блокировки
                await websocket.send_json({
                    "type": "cell_lock_result",
                    "success": success,
                    "cell": data["cell"]
                })
                
            elif data["type"] == "cursor_move":
                await table_sync_manager.sync_cursor_move(
                    table_id, user_id, data["cursor_data"]
                )
                
            elif data["type"] == "ping":
                await websocket.send_json({"type": "pong"})
                
    except WebSocketDisconnect:
        table_sync_manager.disconnect(user_id)
        logger.info(f"User {user_id} disconnected from table {table_id}")
    except Exception as e:
        logger.error(f"Table WS error for user {user_id}: {e}")
        table_sync_manager.disconnect(user_id)