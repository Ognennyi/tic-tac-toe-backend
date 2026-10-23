from uuid import uuid4
from unittest.mock import Mock


from domain.service.auth_service import AuthService
from web.module.user_authenticator import UserAuthenticator


def test_authenticate_success():

    # 1. Создаём поддельный AuthService
    service = Mock(spec=AuthService)

    # 2. Создаём UUID, который хотим получить
    expected_id = uuid4()

    # 3. Настраиваем результат поддельного сервиса
    service.authenticate.return_value = expected_id

    # 4. Создаём тестируемый объект
    authenticator = UserAuthenticator(service)

    # 5. Готовим правильный заголовок
    header = "Basic ZmVuaXg6MTIzNDU2"

    # 6. Вызываем тестируемый метод
    result = authenticator.authenticate(header)

    assert result == expected_id
    service.authenticate.assert_called_once_with((header.split(" ", 1))[1])



def test_authenticate_without_header():

    service = Mock(spec=AuthService)

    service.authenticate.return_value = None
        
    authenticator = UserAuthenticator(service)

    result = authenticator.authenticate(None)

    assert result is None

    service.authenticate.assert_not_called()