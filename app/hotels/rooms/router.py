from datetime import date

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.hotels.rooms.dao import RoomsDao
from app.hotels.rooms.shemas import SRooms

router = APIRouter(prefix="/hotels", tags=["Номера отелей"])


@router.get("/{hotel_id}/rooms")
@cache(expire=60)
async def get_rooms_by_hotel_id(
    hotel_id: int, date_from: date, date_to: date
) -> list[SRooms]:
    """Получить номера отеля с доступностью в указанном периоде"""
    result = await RoomsDao.find_all_rooms(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )
    return result


@router.get("/rooms")
async def get_all_rooms():
    result = await RoomsDao.find_all()
    return result
