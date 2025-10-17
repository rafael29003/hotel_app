import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "date_from,date_to,room_id,status_code",
    [
        # Забронируем все 7 номеров комнаты 10 (quantity=7)
        ("2030-05-19", "2030-05-20", 10, 200),  # 1-й номер
        ("2030-05-19", "2030-05-20", 10, 200),  # 2-й номер
        ("2030-05-19", "2030-05-20", 10, 200),  # 3-й номер
        ("2030-05-19", "2030-05-20", 10, 200),  # 4-й номер
        ("2030-05-19", "2030-05-20", 10, 200),  # 5-й номер
        ("2030-05-19", "2030-05-20", 10, 200),  # 6-й номер
        ("2030-05-19", "2030-05-20", 10, 200),  # 7-й номер (последний)
        ("2030-05-19", "2030-05-20", 10, 409),  # 8-й номер - должен быть конфликт!
    ],
)
async def test_add_booking(
    auth_ac: AsyncClient, date_from, date_to, room_id, status_code
):
    response = await auth_ac.post(
        "/bookings",
        params={
            "date_from": date_from,
            "date_to": date_to,
            "room_id": room_id,
        },
    )

    assert response.status_code == status_code


async def test_get_and_delete(auth_ac: AsyncClient):
    response = await auth_ac.get("/bookings")  # Правильный URL
    assert response.status_code == 200

    bookings = response.json()  # Получаем список бронирований

    for booking in bookings:
        booking_id = booking["id"]  # Получаем ID бронирования
        delete_response = await auth_ac.delete(
            f"/bookings/{booking_id}"
        )  # Правильный URL
        assert delete_response.status_code == 200

    responce = await auth_ac.get("/bookings")
    assert responce.status_code == 400
