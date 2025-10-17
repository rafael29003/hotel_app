from datetime import date

from pydantic import BaseModel


class SBokking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_days: int
    total_price: int

    class Config:
        from_attributes = True
