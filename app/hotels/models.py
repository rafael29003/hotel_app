from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    services: Mapped[list[str]] = mapped_column(JSON)
    room_quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int] = mapped_column(nullable=False)

    hotel_to_room = relationship("Rooms", back_populates="room_to_hotel")

    def __str__(self):
        return f"Отель {self.name}"
