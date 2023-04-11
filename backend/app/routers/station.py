from fastapi import APIRouter, Response, Depends
from database.database import SessionLocal
from database.models import UserSubject
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
def get_station(user: User = Depends(super_user)):
    stations = session.query(UserSubject).all()
    return stations
