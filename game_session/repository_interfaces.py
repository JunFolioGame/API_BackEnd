from abc import ABCMeta, abstractmethod
from uuid import UUID

from game_session.dto import (
    CreateGameSessionDTO,
    GameSessionDTO,
    StatisticsSessionDTOResponse,
)


class AbstractGameSessionRepositoryInterface(metaclass=ABCMeta):
    @abstractmethod
    def create_session(self, game_session_dto: CreateGameSessionDTO) -> GameSessionDTO:
        pass

    @abstractmethod
    def add_player_in_game_session_by_uuid(
        self, session_identificator: str, player_uuid: UUID
    ) -> True:
        pass

    @abstractmethod
    def get_all_players_in_session_by_uuid(
        self, creator_uuid: UUID, session_identificator: str
    ) -> GameSessionDTO:
        pass

    @abstractmethod
    def get_statistics_session(self) -> StatisticsSessionDTOResponse:
        ...
