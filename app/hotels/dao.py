from datetime import date

from sqlalchemy import and_, func, or_, select

from app.bookings.models import Bookings
from app.dao.base import BaseDao
from app.database import async_session_maker
from app.exception import HotelsDateException, HotelsLongException
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelsDAO(BaseDao):
    model = Hotels

    @classmethod
    async def find_all_hotels(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:
            if date_from > date_to:
                raise HotelsDateException
            if (date_to - date_from).days > 30:
                raise HotelsLongException
            bookings_for_selected_dates = (
                select(Bookings).where(
                    and_(Bookings.date_from <= date_to, Bookings.date_to >= date_from)
                )
            ).cte("bookings_for_selected_dates")

            hotels_rooms_left = (
                select(
                    (
                        Hotels.room_quantity
                        - func.count(bookings_for_selected_dates.c.room_id)
                    ).label("rooms_left"),
                    Rooms.hotel_id,
                )
                .select_from(Hotels)
                .outerjoin(Rooms, Rooms.hotel_id == Hotels.id)
                .outerjoin(
                    bookings_for_selected_dates,
                    bookings_for_selected_dates.c.room_id == Rooms.id,
                )
                .where(
                    Hotels.location.like(f"%{location.title()}%"),
                )
                .group_by(Hotels.room_quantity, Rooms.hotel_id)
                .cte("hotels_rooms_left")
            )

            get_hotels_info = (
                select(Hotels.__table__.columns, hotels_rooms_left.c.rooms_left)
                .select_from(Hotels)
                .join(hotels_rooms_left, hotels_rooms_left.c.hotel_id == Hotels.id)
                .where(hotels_rooms_left.c.rooms_left > 0)
            )

            hotels_info = await session.execute(get_hotels_info)
            return hotels_info.mappings().all()
