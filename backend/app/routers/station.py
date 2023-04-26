from fastapi import APIRouter, Response, Depends
from database.database import SessionLocal
from database.models import Station, ControlSensor, ReadSensor
from database.models import User as User_BD
from database.schemas import SensorCreate
from ..auth.users import super_user, current_active_user
from ..auth.db import User

station_router = APIRouter()

session = SessionLocal()


@station_router.post("/create_station/", status_code=201)
def create_station(station_id: int, name: str, response: Response, user: User = Depends(super_user)):
    if session.query(Station).get(station_id):
        response.status_code = 400
        return {"detail": "SUBJECT ALREADY EXISTS"}
    station = Station(id=station_id, name=name)
    session.add(station)
    session.commit()
    return {"detail": "Subject create", "subject": {"id": station_id, "name": name}}


@station_router.post("/bind_station/")
def bind_station(station_id: int, response: Response, user: User = Depends(current_active_user)):
    station = session.query(Station).get(station_id)
    if not station:
        response.status_code = 400
        return {"detail": "STATION DOESN'T EXISTS"}
    station.user_id = user.id
    session.commit()
    return {"detail": f"Success add your station! Your id = {user.id}, station id = {station_id}."}


@station_router.get("/get_stations/")
def get_stations(user: User = Depends(super_user)):
    stations = session.query(Station).all()
    return stations


@station_router.post("/link_sensor/{sensor_id}", status_code=200)
def link_sensor_to_device(response: Response, sensor_id: int, sensor: SensorCreate, user: User = Depends(super_user)):
    sensor_types = {"read": ReadSensor, "control": ControlSensor}
    if sensor.type not in sensor_types:
        response.status_code = 400
        return {"detail": "INVALID TYPE"}
    sensor = sensor_types[sensor.type](id=sensor.id, name=sensor.name, device_id=sensor_id)
    session.add(sensor)
    session.commit()
    return {"detail": "success", "sensor": sensor}
