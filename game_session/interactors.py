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
        game_session_dto = self.service.get_all_players_in_session_by_uuid(
            creator_uuid=creator_uuid, session_identificator=session_identificator
        )
        game_session_dto.lobby = self._sort_teams(
            players=game_session_dto.lobby,
            min_size=game_session_dto.team_players_min,
            max_size=game_session_dto.team_players_max,
            teams_maximum=game_session_dto.team_max,
        )
        return game_session_dto

    def _sort_for_me(self, players: list, n: int) -> dict:
        return [players[x::n] for x in range(n)]

    def _sort_teams(
        self,
        players: list,
        min_size: int,
        max_size: int,
        teams_maximum: int,
    ) -> dict:
        players_amount = len(players)
        for divider in (my_range := range(min_size, max_size + 1)):
            if (
                players_amount % divider == 0
                and (n := players_amount // divider) < teams_maximum + 1
            ):
                return self._sort_for_me(players=players, n=n)
        for divider in my_range:
            if (
                players_amount % divider != 0
                and (n := players_amount // divider) < teams_maximum + 1
            ):
                return self._sort_for_me(players=players, n=n)
