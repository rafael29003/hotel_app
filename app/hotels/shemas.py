from datetime import date
from re import I

from pydantic import BaseModel


class Shotel(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    room_quantity: int
    image_id: int
    rooms_left: int

    class Config:
        from_attributes = True
