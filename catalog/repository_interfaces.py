from abc import ABCMeta, abstractmethod
from uuid import UUID

from catalog.dto import (
    CreateGameInfoDTO,
    FilterSortGameInfoDTORequest,
    GameInfoDTOResponse,
    UpdateGameInfoDTORequest,
)


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

    @abstractmethod
    def catalog_filter_sort(
        self, game_info_filter_sort_dto: FilterSortGameInfoDTORequest
    ) -> list[GameInfoDTOResponse]:
        pass

    @abstractmethod
    def set_like_game_info_by_uuid(
        self, game_info_uuid: UUID, player_uuid: UUID
    ) -> GameInfoDTOResponse:
        pass

    @abstractmethod
    def unset_like_game_info_by_uuid(
        self, game_info_uuid: UUID, player_uuid: UUID
    ) -> GameInfoDTOResponse:
        pass

    @abstractmethod
    def get_statistics_on_the_site(self) -> int:
        pass
