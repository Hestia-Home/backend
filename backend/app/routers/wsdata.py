import time
import asyncio

from log_settings import logger
from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect, WebSocketException
from fastapi.responses import HTMLResponse

from ..auth.users import current_active_user
from database.database import SessionLocal
from database.models import User, Station

from ..fake_data.random_temperature import get_random_temperature_data

ws_router = APIRouter()

session = SessionLocal()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.debug(f"")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        websocket.close()

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_json_message(self, data: dict, websocket: WebSocket):
        await websocket.send_json(data)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@ws_router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    cur_user = session.query(User).get(client_id)
    if not cur_user:
        return {"message": f"User {client_id} doesn't exist"}
    # user_station = session.query(Station)
    try:
        while True:
            data = get_random_temperature_data()
            await manager.send_json_message(data, websocket)
            await asyncio.sleep(30)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
