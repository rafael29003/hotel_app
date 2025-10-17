import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("new@mewnkdfkwnfknwfw.ru", "new11", 200),
        ("new@mewnkdfkwnfknwfw.ru", "newjfbwjf", 409),
        ("abcjsdfjdsfs", "djvnsvbs", 422),
    ],
)
async def test_register(email, password, status_code, ac: AsyncClient):
    result = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    assert result.status_code == status_code


@pytest.mark.parametrize(
    "email , password , status_code",
    [
        ("fedor@moloko.ru", "password123", 200),
        ("sharik@moloko.ru", "password456", 200),
        ("fedor@moloko.ru", "wrongpassword", 401),
    ],
)
async def test_login(email, password, status_code, ac: AsyncClient):
    result = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert result.status_code == status_code
