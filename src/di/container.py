from datasource.repository.game_repository_impl import GameRepositoryImpl
from datasource.database import SessionLocal
from datasource.repository.user_repository_impl import UserRepositoryImpl

from domain.service.user_service_impl import UserServiceImpl
from domain.service.game_service_impl import GameServiceImpl
from domain.service.auth_service_impl import AuthServiceImpl

# SessionLocal    # сама фабрика
# SessionLocal()  # создание конкретной Session

class Container:

    def __init__(self):
        self.session_factory = SessionLocal
        self.repository = GameRepositoryImpl(self.session_factory)
        self.service = GameServiceImpl(self.repository)

        self.user_repository = UserRepositoryImpl(self.session_factory)
        self.user_service = UserServiceImpl(self.user_repository)
        
        self.auth_service = AuthServiceImpl(self.user_service)


