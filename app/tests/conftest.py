import os

os.environ["MODE"] = "TEST"

import asyncio
import json

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.bookings.models import Bookings
from app.config import Settings, settings

# Импортируем database ПОСЛЕ установки MODE
from app.database import Base, async_session_maker, engine
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.main import app as fastapi_app
from app.users.models import Users


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    """Асинхронная фикстура для подготовки БД"""
    assert settings.MODE == "TEST"

    # Очищаем и создаём таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Загружаем тестовые данные
    def open_json(file_name: str):
        with open(f"app/tests/{file_name}", "r") as file:
            return json.load(file)

    users = open_json("users.json")
    hotels = open_json("hotels.json")
    rooms = open_json("rooms.json")
    bookings = open_json("booking.json")

    # Преобразуем строки дат в объекты date для bookings
    from datetime import date

    for booking in bookings:
        booking["date_from"] = date.fromisoformat(booking["date_from"])
        booking["date_to"] = date.fromisoformat(booking["date_to"])

    async with async_session_maker() as session:
        add_hotels = insert(Hotels).values(hotels)
        add_users = insert(Users).values(users)
        add_rooms = insert(Rooms).values(rooms)
        add_bookings = insert(Bookings).values(bookings)

        await session.execute(add_hotels)
        await session.execute(add_users)
        await session.execute(add_rooms)
        await session.execute(add_bookings)
        await session.commit()


@pytest_asyncio.fixture(scope="function")
async def ac():
    """Фикстура для тестирования FastAPI endpoints"""
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://test"
    ) as ac:
        yield ac


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Фикстура для работы с БД в тестах"""
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture(scope="session")
async def auth_ac():
    """Фикстура для тестирования FastAPI endpoints"""
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/auth/login",
            json={
                "email": "fedor@moloko.ru",
                "password": "password123",
            },
        )
        assert response.status_code == 200
        assert "booking_access_token" in response.cookies

        # Сохраняем токен для передачи в следующих запросах
        token = response.cookies["booking_access_token"]

        # Создаем новый клиент с токеном в cookies
        async with AsyncClient(
            transport=ASGITransport(app=fastapi_app),
            base_url="http://test",
            cookies={"booking_access_token": token},
        ) as auth_client:
            yield auth_client
