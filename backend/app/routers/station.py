from fastapi import APIRouter, Response, Depends
from database.database import SessionLocal
from database.models import UserSubject, ControlDevice, ControlSensor, ReaderDevice, ReadSensor
from database.schemas import DeviceCreate, SensorCreate
from ..auth.users import super_user
from ..auth.db import User

station_router = APIRouter()

session = SessionLocal()


@station_router.post("/create_station/", status_code=201)
def create_station(station_id: int, name: str, response: Response, user: User = Depends(super_user)):
    if session.query(UserSubject).get(station_id):
        response.status_code = 400
        return {"detail": "SUBJECT ALREADY EXISTS"}
    station = UserSubject(id=station_id, name=name)
    session.add(station)
    session.commit()
    return {"detail": "Subject create", "subject": {"id": station_id, "name": name}}


@station_router.get("/get_stations/")
def get_stations(user: User = Depends(super_user)):
    stations = session.query(UserSubject).all()
    return stations


@station_router.post("/link_device/{station_id}", status_code=201)
def link_device_to_station(station_id: int, device: DeviceCreate, response: Response, user: User = Depends(super_user)):
    device_types = {"read": ReaderDevice, "control": ControlDevice}
    if device.type not in device_types:
        response.status_code = 400
        return {"detail": "INVALID TYPE"}
    device = device_types[device.type](id=device.id, name=device.name, subject_id=station_id)
    session.add(device)
    session.commit()
    return {"detail": "success", "device": device}


@station_router.post("/link_sensor/{device_id}", status_code=200)
def link_sensor_to_device(response: Response, device_id: int, sensor: SensorCreate, user: User = Depends(super_user)):
    sensor_types = {"read": ReadSensor, "control": ControlSensor}
    if sensor.type not in sensor_types:
        response.status_code = 400
        return {"detail": "INVALID TYPE"}
    sensor = sensor_types[sensor.type](id=sensor.id, name=sensor.name, device_id=device_id)
    session.add(sensor)
    session.commit()
    return {"detail": "success", "sensor": sensor}
