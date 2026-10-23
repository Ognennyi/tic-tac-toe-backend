import base64
from uuid import uuid4

from di.container import Container
from domain.model.sign_up_request import SignUpRequest
from domain.service.auth_service_impl import AuthServiceImpl


def encode_credentials(login: str, password: str) -> str:
    credentials = f"{login}:{password}"
    return base64.b64encode(credentials.encode("utf-8")).decode("ascii")


def test_authenticate():
    container = Container()
    auth_service = AuthServiceImpl(container.user_service)

    login = f"test_{uuid4().hex}"
    password = "correct_password"

    # Регистрируем пользователя
    request = SignUpRequest(login=login, password=password)

    assert auth_service.sign_up(request) is True

    saved_user = container.user_service.get_by_login(login)

    assert saved_user is not None

    # 1. Правильные логин и пароль
    credentials = encode_credentials(login, password)

    assert auth_service.authenticate(credentials) == saved_user.id

    # 2. Неправильный пароль
    wrong_password = encode_credentials(login, "wrong_password")

    assert auth_service.authenticate(wrong_password) is None

    # 3. Несуществующий пользователь
    unknown_login = encode_credentials(f"unknown_{uuid4().hex}", password)

    assert auth_service.authenticate(unknown_login) is None

    # 4. Некорректный Base64
    assert auth_service.authenticate("%%%") is None

    # 5. Нет двоеточия между логином и паролем
    missing_colon = base64.b64encode(b"invalid_format").decode("ascii")

    assert auth_service.authenticate(missing_colon) is None

    # 6. Некорректная UTF-8 строка
    invalid_utf8 = base64.b64encode(b"\xff").decode("ascii")

    assert auth_service.authenticate(invalid_utf8) is None