from abc import abstractmethod, ABCMeta
from uuid import UUID

from catalog.dto import GameInfoDTOResponse, UpdateGameInfoDTORequest, CreateGameInfoDTO


class AbstractGameInfoRepositoryInterface(metaclass=ABCMeta):
    @abstractmethod
    def create_game_info(self, game_info_dto: CreateGameInfoDTO) -> GameInfoDTOResponse:
        pass

    @abstractmethod
    def get_game_info_by_uuid(self, game_info_uuid: UUID) -> GameInfoDTOResponse:
        pass

    @abstractmethod
    def update_game_info_by_uuid(
        self, game_info_to_update: UpdateGameInfoDTORequest
    ) -> GameInfoDTOResponse:
        pass

    @abstractmethod
    def delete_game_info_by_uuid(self, game_info_uuid: UUID) -> dict:
        pass

    @abstractmethod
    def get_all_game_info(self) -> list[GameInfoDTOResponse]:
        pass
