from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == "test"
    assert response.json()['email'] == "test@email.com"
    assert response.json()['first_name'] == "test"
    assert response.json()['last_name'] == "user"
    assert response.json()['role'] == "admin"

def test_change_password_success(test_user):
    request_data = {
        "password": "password",
        "new_password": "newpassword"
    }
    response = client.put("/user/password", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_fail(test_user):
    request_data = {
        "password": "Nopassword",
        "new_password": "newpassword"
    }
    response = client.put("/user/password", json=request_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Unauthorized"}
