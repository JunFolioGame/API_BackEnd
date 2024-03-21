from uuid import UUID

from annoying.functions import get_object_or_None
from django.db.models import Count, Sum, Q
from django.db.models.functions import Coalesce
from django.db import models

from game_session.dto import (
    CreateGameSessionDTO,
    GameSessionDTO,
    StatisticsSessionDTOResponse,
)
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
        if not game_session or not game_session.is_active:
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
        if not game_session or not game_session.is_active:
            raise GameSessionDoesNotExist()
        lobby = [
            {str(player.player_uuid): player.username}
            for player in game_session.lobby.all()
        ]
        if len(lobby) < game_session.team_min * game_session.team_players_min:
            raise GameSessionNotEnough()
        lobby, teams = self._sort_teams(
            players=lobby,
            min_size=game_session.team_players_min,
            max_size=game_session.team_players_max,
            teams_maximum=game_session.team_max,
        )
        result = self._game_session_to_dto(game_session=game_session, lobby=lobby)
        game_session.is_active = False
        game_session.final_teams = teams
        game_session.save()
        return result

    def _sort_for_me(self, players: list, n: int) -> tuple[list, int]:
        return ([players[x::n] for x in range(n)], n)

    def _sort_teams(
        self,
        players: list,
        min_size: int,
        max_size: int,
        teams_maximum: int,
    ) -> tuple[list, int]:
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

    def get_statistics_session(self) -> StatisticsSessionDTOResponse:
        try:
            result = GameSession.objects.aggregate(
                number_of_teams=Coalesce(Sum("final_teams"), 0),
                played=Coalesce(Count("pk", filter=Q(is_active=False)), 0),
            )
        except models.ObjectDoesNotExist:
            result = {"played": 0, "number_of_teams": 0}
        return StatisticsSessionDTOResponse(**result)
