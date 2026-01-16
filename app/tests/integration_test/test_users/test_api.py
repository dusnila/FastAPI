from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("email, password, status_code",[
    ("kot@pes.com", "kotopes", 200),
    ("kot@pes.com", "kotopes", 409),
    ("pes@kot.com", "kotopes", 200),
    ("asdfdsag", "kotopes", 422),
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    responcse = await ac.post("/auth/register", json={
        "email": email,
        "password": password
    })

    assert responcse.status_code == status_code

@pytest.mark.parametrize("email, password, status_code",[
    ("test@test.com", "test", 200),
    ("artem@example.com", "artem", 200),
    ("wrong@person.com", "kotopes", 401),
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    responcse = await ac.post("/auth/login", json={
        "email": email,
        "password": password
    })
    
    assert responcse.status_code == status_code