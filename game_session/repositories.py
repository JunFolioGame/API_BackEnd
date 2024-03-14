from uuid import UUID

from annoying.functions import get_object_or_None

from game_session.dto import CreateGameSessionDTO, GameSessionDTO
from game_session.exceptions import (
    GameSessionDoesNotExist,
    GameSessionFull,
    GameSessionNotEnough,
)
from game_session.models import GameSession
from game_session.repository_interfaces import AbstractGameSessionRepositoryInterface
from players.models import Player


class GameSessionRepository(AbstractGameSessionRepositoryInterface):
    def create_session(self, game_session_dto: CreateGameSessionDTO) -> GameSessionDTO:
        game_session = GameSession.objects.create(
            creator=Player(player_uuid=game_session_dto.creator_uuid),
            team_min=game_session_dto.team_min,
            team_max=game_session_dto.team_max,
            team_players_min=game_session_dto.team_players_min,
            team_players_max=game_session_dto.team_players_max,
        )
        return self._game_session_to_dto(game_session=game_session)

    def add_player_in_game_session_by_uuid(
        self, session_identificator: str, player_uuid: UUID
    ) -> True:
        game_session = get_object_or_None(
            GameSession, identificator=session_identificator
        )
        if not game_session:
            raise GameSessionDoesNotExist()
        if (
            game_session.lobby
            and game_session.lobby.count() + 1
            > game_session.team_max * game_session.team_players_max
        ):
            raise GameSessionFull()
        game_session.lobby.add(*[player_uuid])
        return True

    def get_all_players_in_session_by_uuid(
        self, creator_uuid: UUID, session_identificator: str
    ) -> GameSessionDTO:
        game_session = (
            GameSession.objects.filter(
                identificator=session_identificator, creator=creator_uuid
            )
            .prefetch_related("lobby")
            .first()
        )
        if not game_session:
            raise GameSessionDoesNotExist()
        lobby = [player.player_uuid for player in game_session.lobby.all()]
        if len(lobby) < game_session.team_min * game_session.team_players_min:
            raise GameSessionNotEnough()
        result = self._game_session_to_dto(game_session=game_session, lobby=lobby)
        game_session.delete()
        return result

    def _game_session_to_dto(
        self, game_session: GameSession, lobby: list = [[]]
    ) -> GameSessionDTO:
        return GameSessionDTO(
            session_identificator=game_session.identificator,
            team_min=game_session.team_min,
            team_max=game_session.team_max,
            team_players_min=game_session.team_players_min,
            team_players_max=game_session.team_players_max,
            lobby=lobby,
        )
