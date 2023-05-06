from pydantic import BaseModel


class SensorCreate(BaseModel):
    id: int
    name: str
    type: str
