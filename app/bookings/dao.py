from datetime import date

from sqlalchemy import and_, delete, func, insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.dao.base import BaseDao
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.logger import logger


class BookingDao(BaseDao):
    model = Bookings

    @classmethod
    async def create_booking(
        cls, date_from: date, date_to: date, room_id: int, user_id: int
    ):
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
            (date_from <= '2023-06-20' and date_to >= '2023-05-15' )
        )
        SELECT rooms.quantity - count(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON rooms.id = booked_rooms.room_id
        WHERE rooms.id = 1
        group by rooms.quantity , booked_rooms.room_id
        """
        # Создаем CTE для забронированных комнат
        try:
            async with async_session_maker() as session:
                booked_rooms_cte = (
                    select(Bookings.room_id)
                    .where(
                        and_(
                            Bookings.room_id == room_id,
                            and_(
                                Bookings.date_from <= date_to,
                                Bookings.date_to >= date_from,
                            ),
                        )
                    )
                    .cte("booked_rooms")
                )

                # Основной запрос для подсчета свободных комнат
                get_rooms_left = (
                    select(Rooms.quantity - func.count(booked_rooms_cte.c.room_id))
                    .select_from(Rooms)
                    .join(
                        booked_rooms_cte,
                        Rooms.id == booked_rooms_cte.c.room_id,
                        isouter=True,
                    )
                    .where(Rooms.id == room_id)
                    .group_by(Rooms.quantity, booked_rooms_cte.c.room_id)
                )

                result = await session.execute(get_rooms_left)
                rooms_value: int = result.scalar_one_or_none()

                if rooms_value and rooms_value > 0:
                    query = select(Rooms.price).where(Rooms.id == room_id)
                    price_value = await session.execute(query)
                    price: int = price_value.scalar()

                    add_booking = (
                        insert(Bookings)
                        .values(
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                            user_id=user_id,
                            room_id=room_id,
                        )
                        .returning(Bookings.__table__.columns)
                    )

                    booking_result = await session.execute(add_booking)
                    await session.commit()
                    return booking_result.mappings().first()
                else:
                    return None
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database error"
                extra = {
                    "date_from": date_from,
                    "date_to": date_to,
                    "room_id": room_id,
                    "user_id": user_id,
                }
            else:
                msg = "Unknown error"
                extra = {
                    "date_from": date_from,
                    "date_to": date_to,
                    "room_id": room_id,
                    "user_id": user_id,
                }
            logger.error(msg, extra=extra, exc_info=True)
