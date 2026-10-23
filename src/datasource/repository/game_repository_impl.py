from uuid import UUID

from datasource.mapper.game_mapper import to_datasource, to_domain
from domain.model.game import Game as DomainGame

from datasource.repository.game_repository import GameRepository

from datasource.model.game import Game as DatasourceGame
from sqlalchemy import select


class GameRepositoryImpl(GameRepository):

    def __init__(self, session_factory):
        self.session_factory = session_factory


    def save(self, game: DomainGame) -> None:        #Чтобы принимал domainGame

        datasource_game = to_datasource(game)
        with self.session_factory.begin() as session:
            session.merge(datasource_game)

        


    def get(self, game_id: UUID) -> DomainGame | None:

        with self.session_factory() as session:
            datasource_game = session.get(DatasourceGame, game_id)

            if datasource_game is None:
                return None
            
            domain_game = to_domain(datasource_game)
            return domain_game


    
    def get_available_games(self) -> list[DomainGame]:

        with self.session_factory() as session:
            result = select(DatasourceGame).where(
                DatasourceGame.game_status == "waiting",
                DatasourceGame.is_computer_game == False,
                DatasourceGame.player_2_id.is_(None)
            )

            games = session.scalars(result).all()

            games_list = []
            for game in games:
                games_list.append(to_domain(game))

            return games_list 

