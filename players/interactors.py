from uuid import UUID

from players.dto import PlayerDTO
from players.services_interfaces import AbstractPlayerServiceInterface


class PlayerInteractor:
    def __init__(self, player_service: AbstractPlayerServiceInterface):
        self.player_service = player_service

    def create_player(self) -> PlayerDTO:
        return self.player_service.create_player()

    def update_player(self, player: PlayerDTO) -> PlayerDTO:
        return self.player_service.update_player(player=player)

    def get_player_by_uuid(self, player_uuid: UUID) -> PlayerDTO:
        return self.player_service.get_player_by_uuid(player_uuid=player_uuid)
