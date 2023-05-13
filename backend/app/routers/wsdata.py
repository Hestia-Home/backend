import asyncio

from log_settings import logger
from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect
# from fastapi.responses import HTMLResponse

# from ..auth.users import current_active_user
from database.database import SessionLocal
from database.models import User

# from ..fake_data.random_temperature import get_random_temperature_data

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

    @staticmethod
    async def send_personal_message(message: str, websocket: WebSocket):
        await websocket.send_text(message)

    @staticmethod
    async def send_json_message(data: dict, websocket: WebSocket):
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
        old_data = get_only_devices(stations)
        try:
            while True:
                session.commit()
                cur_data = get_only_devices(stations)
                for old_device, new_device in zip(old_data, cur_data):
                    if old_device["id"] == new_device["id"] and old_device["data"] != new_device["data"]:
                        logger.debug(f"User {client_id} get device data:\n {new_device}")
                        await manager.send_json_message(new_device, websocket)
                        # await asyncio.sleep(1)
                        old_data = cur_data
                await asyncio.sleep(2)

                # print(data)
                # print("***")
                # print(cur_data)
                # if data != cur_data:
                #     await manager.send_json_message(cur_data, websocket)
                #     data = cur_data
                #     await asyncio.sleep(15)
                # await asyncio.sleep(5)
        except WebSocketDisconnect:
            manager.disconnect(websocket)


def get_devices_with_station(stations):
    data = {}
    for station in stations:
        data[f"Station {station.id}"] = []
        for device in station.devices:
            data[f"Station {station.id}"].append({"id": device.id, "device_type": device.type,
                                                  "data": device.data, "time": device.time})
    return data


def get_only_devices(stations):
    data = []
    for station in stations:
        for device in station.devices:
            dct = {"id": device.id, "device_type": device.type, "data": device.data, "time": device.time}
            data.append(dct)
    return data
