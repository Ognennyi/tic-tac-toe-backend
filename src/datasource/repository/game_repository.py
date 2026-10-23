from abc import ABC, abstractmethod
from uuid import UUID

from datasource.model.game import Game as DataSourceGame
from domain.model.game import Game as DomainGame


class GameRepository(ABC):

    @abstractmethod
    def save(self, game: DomainGame) -> None:
        pass

    @abstractmethod
    def get(self, game_id: UUID) -> DomainGame | None:
        pass

    @abstractmethod
    def get_available_games(self) -> list[DomainGame]:
        pass


