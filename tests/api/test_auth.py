from __future__ import annotations


def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Grace Hopper",
            "email": "grace@example.com",
            "password": "supersecret123",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "grace@example.com"
    assert body["role"] == "member"
    assert body["is_active"] is True


def test_login_returns_bearer_token(client, seeded_user):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": seeded_user.email, "password": "secret123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_me_returns_current_user(client, user_token):
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == "ada@example.com"


def test_login_rejects_invalid_password(client, seeded_user):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": seeded_user.email, "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

