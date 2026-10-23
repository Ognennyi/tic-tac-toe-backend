import base64
from uuid import uuid4

from app import app, container


def encode_credentials(login: str, password: str) -> str:
    credentials = f"{login}:{password}"
    return base64.b64encode(
        credentials.encode("utf-8")
    ).decode("ascii")


def test_login_success():
    client = app.test_client()

    login = f"test_{uuid4().hex}"
    password = "correct_password"

    signup_response = client.post(
        "/auth/signup",
        json={"login": login, "password": password}
    )

    assert signup_response.status_code == 201

    saved_user = container.user_service.get_by_login(login)
    assert saved_user is not None

    credentials = encode_credentials(login, password)

    response = client.post(
        "/auth/login",
        headers={"Authorization": f"Basic {credentials}"}
    )

    print(response.get_json())

    assert response.status_code == 200
    assert response.get_json()["user_id"] == str(saved_user.id)


def test_login_invalid_credentials():
    client = app.test_client()

    login = f"test_{uuid4().hex}"
    password = "correct_password"

    signup_response = client.post(
        "/auth/signup",
        json={"login": login, "password": password}
    )

    assert signup_response.status_code == 201

    correct_credentials = encode_credentials(login, password)

    invalid_headers = [
        {},  # Нет заголовка
        {"Authorization": "Basic"},  # Нет Base64-строки
        {"Authorization": "Basic "},  # Пустая строка
        {"Authorization": f"Bearer {correct_credentials}"},  # Не Basic
        {"Authorization": "Basic %%%"},  # Неверный Base64
        {
            "Authorization": (
                f"Basic {encode_credentials(login, 'wrong_password')}"
            )
        },
        {
            "Authorization": (
                f"Basic {encode_credentials('unknown_user', password)}"
            )
        },
    ]

    for headers in invalid_headers:
        response = client.post("/auth/login", headers=headers)

        assert response.status_code == 401, (
            f"Заголовки: {headers}, получен статус: {response.status_code}"
        )

        assert response.headers.get("WWW-Authenticate") == (
            'Basic realm="TicTacToe"'
        )