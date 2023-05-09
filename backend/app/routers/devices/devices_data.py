from datetime import datetime

from fastapi import APIRouter, Response

from database.database import SessionLocal
from database.models import Device
from database.schemas import DeviceData

router_device = APIRouter()

session = SessionLocal()


@router_device.put("/send_data/{device_id}")
def update_data_from_devices(device_id: int, response: Response, data: DeviceData):
    device = Device
    cur_device = session.query(device).get(device_id)
    if not cur_device:
        response.status_code = 400
        return {"message": "device doesn't exist"}
    cur_device.data = data.value
    time_now = datetime.utcnow()
    cur_device.time = time_now
    session.commit()
    return {"message": "success update", "device_id": device_id, "value": data.value, "time": time_now}