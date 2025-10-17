from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from fastapi_versioning import version

from app.bookings.dao import BookingDao
from app.bookings.schemas import SBokking
from app.exception import (
    BookingNotFoundException,
    NobookingsException,
    RoomIsNotAvailableException,
)
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_all_bookings(user: Users = Depends(get_current_user)) -> list[SBokking]:
    result = await BookingDao.find_all(user_id=user.id)
    if result == []:
        raise NobookingsException()
    else:
        return result


@router.delete("/{booking_id}")
async def delete_by_id(booking_id: int, user: Users = Depends(get_current_user)):
    """Удалить бронирование по ID (только свое бронирование)"""
    deleted_count = await BookingDao.delete_by_filter(id=booking_id, user_id=user.id)
    if deleted_count == 0:
        raise BookingNotFoundException()

    return {
        "message": f"Бронирование {booking_id} успешно удалено",
        "deleted_count": deleted_count,
    }


@router.post("")
async def add_booking(
    date_from: date,
    date_to: date,
    room_id: int,
    user: Users = Depends(get_current_user),
):
    result_booking = await BookingDao.create_booking(
        date_from=date_from, date_to=date_to, room_id=room_id, user_id=user.id
    )

    if result_booking:
        booking_dict = dict(result_booking)
        send_booking_confirmation_email.delay(booking_dict, user.email)
        return {"message": "Бронирование успешно добавлено"}
    else:
        raise RoomIsNotAvailableException()
