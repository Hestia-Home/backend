from pydantic import BaseModel


class DeviceData(BaseModel):
    id: int
    # device_type: int
    data: str
    status: bool


class StationData(BaseModel):
    id: int
    devices: list[DeviceData]
