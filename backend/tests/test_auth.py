"""
Тестирование endpoint'ов для аунтентификации пользователя.
"""

from conftest import client
import time


class TestUserAuthentication:
    def test_register_and_login_client(self):
        response = client.post("/auth/register",
                               json={
                                   "email": "user@example.com",
                                   "password": "string",
                                   "is_active": True,
                                   "is_superuser": False,
                                   "is_verified": False,
                                   "username": "string"
                               })

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "user@example.com"
        assert data["is_active"] is True
        assert data["is_superuser"] is False
        assert data["is_verified"] is False
        assert data["username"] == "string"
        assert "password" not in data
        assert "hashed_password" not in data
        client.post("/login")

        response = client.post("/auth/jwt/login", data={"username": "user@example.com", "password": "string"})
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data and data["token_type"] == "bearer"
        access_token = data["access_token"]
        # response = client.get("/authenticated-route")
        # assert response.status_code == 200
        # print(response.text)
