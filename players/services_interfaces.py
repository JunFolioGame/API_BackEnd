from abc import ABCMeta, abstractmethod
from uuid import UUID

from players.dto import CreatePlayerDTO, PlayerDTO


class AbstractPlayerServiceInterface(metaclass=ABCMeta):
    @abstractmethod
    def create_player(self, player: CreatePlayerDTO) -> PlayerDTO:
        pass

    @abstractmethod
    def update_player(self, player: PlayerDTO) -> PlayerDTO:
        pass

    @abstractmethod
    def get_player_by_options(self, player: CreatePlayerDTO) -> PlayerDTO:
        pass

    @abstractmethod
    def get_player_by_uuid(self, player_uuid: UUID) -> PlayerDTO:
        pass
