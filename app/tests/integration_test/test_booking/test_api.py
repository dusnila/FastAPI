from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("room_id,date_from,date_to,status_code, expected_count",[
    *[(4, "2023-05-01", "2023-05-24", 200, i) for i in range(3, 11)],
    (4, "2023-05-01", "2023-05-24", 409, 10),
    (4, "2023-05-01", "2023-05-24", 409, 10),
])
async def test_add_and_get_booking(room_id, date_from, date_to, status_code, expected_count, authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/booking", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })

    assert response.status_code == status_code

    response = await authenticated_ac.get("/booking")

    assert len(response.json()) == expected_count
