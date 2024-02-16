from uuid import UUID

from annoying.functions import get_object_or_None

from players.dto import CreatePlayerDTO, PlayerDTO
from players.exceptions import PlayerDoesNotExist
from players.models import Player
from players.repository_interfaces import AbstractPlayerRepositoryInterface


class PlayerRepository(AbstractPlayerRepositoryInterface):

    def create_player(self, player: CreatePlayerDTO) -> PlayerDTO:
        player = Player.objects.create(
            api_adress=player.api_adress, browser_info=player.browser_info
        )
        return self._player_to_dto(player)

    def update_player(self, player: PlayerDTO) -> PlayerDTO:
        player_to_update = Player.objects.filter(player_uuid=player.player_uuid)
        if not player:
            raise PlayerDoesNotExist()
        player_to_update.update(
            api_adress=player.api_adress,
            browser_info=player.browser_info,
            username=player.username,
        )
        player = player_to_update.get()
        return self._player_to_dto(player)

    def get_player_by_options(self, player: CreatePlayerDTO) -> PlayerDTO:
        player = get_object_or_None(
            Player, api_adress=player.api_adress, browser_info=player.browser_info
        )
        if not player:
            raise PlayerDoesNotExist()
        return self._player_to_dto(player=player)

    def get_player_by_uuid(self, player_uuid: UUID) -> PlayerDTO:
        player = get_object_or_None(Player, player_uuid=player_uuid)
        if not player:
            raise PlayerDoesNotExist()
        return self._player_to_dto(player=player)

    def _player_to_dto(self, player: Player) -> PlayerDTO:
        return PlayerDTO(
            player_uuid=player.player_uuid,
            api_adress=player.api_adress,
            browser_info=player.browser_info,
            username=player.username,
        )
