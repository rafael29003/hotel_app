import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "date_from , date_to , location , status_code",
    [
        ("2025-05-19", "2025-05-20", "Алтай", 200),
        ("2025-05-20", "2025-05-19", "Алтай", 400),
        ("2025-05-19", "2025-06-19", "Алтай", 400),
    ],
)
async def test_get_all_hotels(
    ac: AsyncClient, date_from, date_to, location, status_code
):
    response = await ac.get(
        f"/hotels/location/{location}",
        params={
            "location": location,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code
