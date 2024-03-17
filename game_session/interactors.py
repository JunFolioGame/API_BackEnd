from uuid import UUID

from game_session.dto import CreateGameSessionDTO, GameSessionDTO
from game_session.services_interfaces import AbstractGameSessionServiceInterface


class GameSessionInteractor:
    def __init__(self, service: AbstractGameSessionServiceInterface):
        self.service = service

    def create_session(self, game_session_dto: CreateGameSessionDTO) -> GameSessionDTO:
        return self.service.create_session(game_session_dto=game_session_dto)

    def add_player_in_game_session_by_uuid(
        self, session_identificator: str, player_uuid: UUID
    ) -> True:
        return self.service.add_player_in_game_session_by_uuid(
            session_identificator=session_identificator, player_uuid=player_uuid
        )

    def get_all_players_in_session_by_uuid(
        self, creator_uuid: UUID, session_identificator: str
    ) -> GameSessionDTO:
        return self.service.get_all_players_in_session_by_uuid(
            creator_uuid=creator_uuid, session_identificator=session_identificator
        )
