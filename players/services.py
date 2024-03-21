from uuid import UUID

from players.dto import PlayerDTO
from players.repository_interfaces import AbstractPlayerRepositoryInterface
from players.services_interfaces import AbstractPlayerServiceInterface


class PlayerService(AbstractPlayerServiceInterface):
    def __init__(self, repository: AbstractPlayerRepositoryInterface):
        self.repository = repository

    def create_player(self) -> PlayerDTO:
        return self.repository.create_player()

    def update_player(self, player: PlayerDTO) -> PlayerDTO:
        return self.repository.update_player(player=player)

    def get_player_by_uuid(self, player_uuid: UUID) -> PlayerDTO:
        return self.repository.get_player_by_uuid(player_uuid=player_uuid)
