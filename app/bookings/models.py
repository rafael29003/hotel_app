from datetime import datetime

from sqlalchemy import JSON, Column, Computed, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[datetime] = mapped_column(Date, nullable=False)
    date_to: Mapped[datetime] = mapped_column(Date, nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    total_days: Mapped[int] = mapped_column(Computed("date_to - date_from"))
    total_price: Mapped[int] = mapped_column(Computed("(date_to - date_from) * price"))

    booking_to_user = relationship("Users", back_populates="user_to_booking")
    booking_to_room = relationship("Rooms", back_populates="room_to_booking")

    def __str__(self):
        return f"Бронирование {self.id}"
