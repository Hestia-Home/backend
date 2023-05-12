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
        logger.debug(f"User {client_id} can't connect to websocket, because user doesn't exist")
        await manager.send_personal_message(f"User-{client_id} doesn't exist.", websocket)
    else:
        logger.debug(f"User {client_id} has connect to websocket")
        stations = cur_user.stations
        data = get_devices(stations)
        try:
            while True:
                session.commit()
                cur_data = get_devices(stations)
                # print(cur_data)
                # print()
                # print(data)
                if data != cur_data:
                    await manager.send_json_message(cur_data, websocket)
                    data = cur_data
                    await asyncio.sleep(15)
                await asyncio.sleep(5)
        except WebSocketDisconnect:
            manager.disconnect(websocket)


def get_devices(stations):
    data = {}
    for station in stations:
        data[f"Station {station.id}"] = []
        for device in station.devices:
            data[f"Station {station.id}"].append({"id": device.id, "device_type": device.type,
                                                  "data": device.data, "time": device.time})
    return data
