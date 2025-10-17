from sqlalchemy import JSON, Column, Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    user_to_booking = relationship("Bookings", back_populates="booking_to_user")

    def __str__(self):
        return f"User {self.email}"
