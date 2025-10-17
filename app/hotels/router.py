import asyncio
from datetime import date

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelsDAO
from app.hotels.shemas import Shotel

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("")
@cache(expire=60)
async def get_all_hotels():
    result = await HotelsDAO.find_all()
    return result


@router.get("/location/{location}")
async def get_hotels_by_location(
    location: str,
    date_from: date = Query(..., description="Дата заезда"),
    date_to: date = Query(..., description="Дата выезда"),
) -> list[Shotel]:
    """
    Получить список отелей по местоположению с доступными номерами

    - **location**: Местоположение отеля (частичное совпадение)
    - **date_from**: Дата заезда
    - **date_to**: Дата выезда

    Возвращает только отели с минимум 1 свободным номером в указанном периоде
    """
    return await HotelsDAO.find_all_hotels(
        location=location, date_from=date_from, date_to=date_to
    )
