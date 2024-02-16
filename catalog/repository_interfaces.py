from abc import abstractmethod, ABCMeta
from uuid import UUID

from catalog.dto import GameInfoDTO, UpdateGameInfoDTO, CreateGameInfoDTO


class AbstractGameInfoRepositoryInterface(metaclass=ABCMeta):
    @abstractmethod
    def create_game_info(self, game_info_dto: CreateGameInfoDTO) -> GameInfoDTO:
        pass

    @abstractmethod
    def get_game_info_by_uuid(self, game_info_uuid: UUID) -> GameInfoDTO:
        pass

    @abstractmethod
    def update_game_info_by_uuid(
        self, game_info_to_update: UpdateGameInfoDTO
    ) -> GameInfoDTO:
        pass

    @abstractmethod
    def delete_game_info_by_uuid(self, game_info_uuid: UUID) -> None:
        pass

    @abstractmethod
    def get_all_game_info(self) -> list[GameInfoDTO]:
        pass
