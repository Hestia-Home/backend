from datetime import datetime
from fastapi import APIRouter, Response
from .schemas import SensorData
from database.database import SessionLocal
from database.models import Sensor

router_sensors = APIRouter()

session = SessionLocal()


@router_sensors.put("/send_data/{sensor_id}")
def update_data_from_sensors(sensor_id: int, response: Response, data: SensorData):
    sensor = Sensor
    cur_sensor = session.query(sensor).get(sensor_id)
    if not cur_sensor:
        response.status_code = 400
        return {"message": "sensor doesn't exist"}
    cur_sensor.data = data.value
    time_now = datetime.utcnow()
    cur_sensor.time = time_now
    session.commit()
    return {"message": "success update", "sensor_id": sensor_id, "value": data.value, "time": time_now}
