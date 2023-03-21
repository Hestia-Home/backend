import time
import asyncio

from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect, WebSocketException
from fastapi.responses import HTMLResponse

from ..dependencies import get_random_data

ws_router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        # print("Hello user!")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

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
    try:
        # for _ in range(10):
        while True:
        # websocket.receive_text()
            data = get_random_data()
            await manager.send_json_message(data, websocket)
            await asyncio.sleep(30)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # except WebSocketException:
        #     manager.disconnect(websocket)