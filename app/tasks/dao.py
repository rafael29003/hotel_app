from datetime import date, timedelta

from sqlalchemy import select

from app.bookings.models import Bookings
from app.dao.base import BaseDao
from app.database import async_session_maker
from app.users.dao import UsersDAO
from app.users.models import Users


class SendDao(BaseDao):
    model = Bookings

    @classmethod
    async def users_bookings_for_tomorrow(cls, days: int):
        async with async_session_maker() as session:
            bookings_start_tomorrow = (
                select(Bookings.__table__.columns)
                .where(Bookings.date_from == date.today() + timedelta(days=days))
                .cte("bookings_start_tomorrow")
            )

            user_with_bookings = (
                select(
                    Users.email,
                    bookings_start_tomorrow.c.date_from,
                    bookings_start_tomorrow.c.date_to,
                    bookings_start_tomorrow.c.price,
                    bookings_start_tomorrow.c.total_days,
                    bookings_start_tomorrow.c.total_price,
                )
                .select_from(Users)
                .join(
                    bookings_start_tomorrow,
                    Users.id == bookings_start_tomorrow.c.user_id,
                )
            )

            result = await session.execute(user_with_bookings)
            return result.mappings().all()
