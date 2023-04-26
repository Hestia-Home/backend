from pydantic import BaseModel


class SensorData(BaseModel):
    # id: int
    value: str
    type: int
