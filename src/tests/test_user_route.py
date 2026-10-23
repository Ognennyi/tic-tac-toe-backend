import base64

from uuid import uuid4

from app import app, container


def create_auth_header(login, password):
    credentials = f"{login}:{password}"
    encoded = base64.b64encode(credentials.encode()).decode()

    return {
        "Authorization": f"Basic {encoded}"
    }


def test_get_user_by_id():
    client = app.test_client()

    login = f"user_{uuid4().hex}"
    password = "123456"

    client.post(
        "/auth/signup",
        json={
            "login": login,
            "password": password
        }
    )

    user = container.user_service.get_by_login(login)

    headers = create_auth_header(login, password)

    response = client.get(
        f"/users/{user.id}",
        headers=headers
    )

    assert response.status_code == 200

    assert response.get_json() == {
        "id": str(user.id),
        "login": login
    }


def test_get_user_by_id_not_found():
    client = app.test_client()

    login = f"user_{uuid4().hex}"
    password = "123456"

    client.post(
        "/auth/signup",
        json={
            "login": login,
            "password": password
        }
    )

    headers = create_auth_header(login, password)

    unknown_user_id = uuid4()

    response = client.get(
        f"/users/{unknown_user_id}",
        headers=headers
    )

    assert response.status_code == 404

    assert response.get_json() == {
        "message": "Пользователь не найден"
    }