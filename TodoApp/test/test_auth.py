from .utils import *
from ..routers.auth import get_db, get_current_user, authenticate_user
from fastapi import status
import pytest

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, "password", db)  
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user = authenticate_user("non_existent_user", "password", db)
    assert non_existent_user is False

    wrong_password = authenticate_user(test_user.username, "wrong_password", db)
    assert wrong_password is False