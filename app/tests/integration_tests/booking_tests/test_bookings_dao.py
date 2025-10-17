from datetime import datetime

from app.bookings.dao import BookingDao


async def test_crud_operation():
    result = await BookingDao.create_booking(
        date_from=datetime.strptime("2023-05-19", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-05-19", "%Y-%m-%d"),
        room_id=11,
        user_id=3,
    )

    assert result.user_id == 3

    read_result = await BookingDao.find_by_id(result.id)

    assert read_result.id == result.id

    deleted = await BookingDao.delete_by_filter(id=result.id)
    assert deleted == 1

    read_result = await BookingDao.find_by_id(result.id)
    assert read_result is None
