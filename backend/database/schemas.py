from pydantic import BaseModel


class DeviceCreate(BaseModel):
    id: int
    name: str
    type: str


class SensorCreate(BaseModel):
    id: int
    name: str
    type: str