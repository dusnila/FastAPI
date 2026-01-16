

import pytest
from app.users.service import UsersService

@pytest.mark.parametrize("user_id, email, exists", [
   (1, "test@test.com" ,True),
   (2, "artem@example.com" ,True),
   (3, "..." ,False)
])
async def test_find_users_by_id(user_id, email, exists):
    user = await UsersService.find_by_id(user_id)

    if exists:
        assert user
        assert user.id == user_id
        assert user.email == email
    if not exists:
        assert not user