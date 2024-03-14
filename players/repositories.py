from uuid import UUID

from annoying.functions import get_object_or_None
from django.core.exceptions import ValidationError

from players.dto import PlayerDTO
from players.exceptions import PlayerDoesNotExist, WrongUUID
from players.models import Player
from players.repository_interfaces import AbstractPlayerRepositoryInterface


class PlayerRepository(AbstractPlayerRepositoryInterface):

    def create_player(self) -> PlayerDTO:
        player = Player.objects.create()
        return self._player_to_dto(player)

    def update_player(self, player: PlayerDTO) -> PlayerDTO:
        try:
            player_to_update = Player.objects.filter(player_uuid=player.player_uuid)
        except ValidationError:
            raise WrongUUID(value=player.player_uuid)
        if not player_to_update:
            raise PlayerDoesNotExist()
        player_to_update.update(
            username=player.username,
        )
        player = player_to_update.get()
        return self._player_to_dto(player)

    def get_player_by_uuid(self, player_uuid: UUID) -> PlayerDTO:
        try:
            player = get_object_or_None(Player, player_uuid=player_uuid)
        except ValidationError:
            raise WrongUUID(value=player_uuid)
        if not player:
            raise PlayerDoesNotExist()
        return self._player_to_dto(player=player)

    def _player_to_dto(self, player: Player) -> PlayerDTO:
        return PlayerDTO(
            player_uuid=player.player_uuid,
            username=player.username,
        )
