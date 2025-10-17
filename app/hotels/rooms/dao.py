from datetime import date

from sqlalchemy import and_, func, select

from app.bookings.models import Bookings
from app.dao.base import BaseDao
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.hotels.rooms.shemas import SRooms


class RoomsDao(BaseDao):
    model = Rooms

    @classmethod
    async def find_all_rooms(
        cls, hotel_id: int, date_from: date, date_to: date
    ) -> list[SRooms]:
        async with async_session_maker() as session:
            bookings_for_selected_dates = (
                select(Bookings)
                .join(Rooms)
                .where(
                    and_(
                        Rooms.hotel_id == hotel_id,
                        and_(
                            Bookings.date_from <= date_to, Bookings.date_to >= date_from
                        ),
                    )
                )
                .cte("bookings_for_selected_dates")
            )

            rooms_left = (
                select(
                    (
                        Rooms.quantity
                        - func.count(bookings_for_selected_dates.c.room_id)
                    ).label("rooms_left"),
                    Rooms.id.label("room_id"),
                )
                .select_from(Rooms)
                .outerjoin(
                    bookings_for_selected_dates,
                    Rooms.id == bookings_for_selected_dates.c.room_id,
                )
                .where(Rooms.hotel_id == hotel_id)
                .group_by(Rooms.quantity, Rooms.id)
                .cte("rooms_left")
            )

            get_rooms_info = (
                select(
                    Rooms.__table__.columns,
                    (Rooms.price * Rooms.quantity).label("total_cost"),
                    rooms_left.c.rooms_left,
                )
                .select_from(Rooms)
                .join(rooms_left, Rooms.id == rooms_left.c.room_id)
                .where(rooms_left.c.rooms_left > 0)
            )

            result = await session.execute(get_rooms_info)
            return result.mappings().all()
