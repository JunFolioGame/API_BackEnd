from uuid import UUID

from catalog.dto import (
    GameInfoDTOResponse,
    CreateGameInfoDTO,
    UpdateGameInfoDTORequest,
    FilterSortGameInfoDTORequest,
)
from catalog.repository_interfaces import AbstractGameInfoRepositoryInterface
from catalog.services_interfaces import GameInfoServiceInterface


class GameInfoService(GameInfoServiceInterface):
    def __init__(self, repository: AbstractGameInfoRepositoryInterface):
        self.repository = repository

    def create_game_info(self, game_info_dto: CreateGameInfoDTO) -> GameInfoDTOResponse:
        return self.repository.create_game_info(game_info_dto)

    def get_game_info_by_uuid(self, game_info_uuid: UUID) -> GameInfoDTOResponse:
        return self.repository.get_game_info_by_uuid(game_info_uuid)

    def update_game_info_by_uuid(
        self, game_info_to_update: UpdateGameInfoDTORequest
    ) -> GameInfoDTOResponse:
        return self.repository.update_game_info_by_uuid(game_info_to_update)

    def delete_game_info_by_uuid(self, game_info_uuid: UUID) -> dict:
        return self.repository.delete_game_info_by_uuid(game_info_uuid)

    def get_all_game_info(self) -> list[GameInfoDTOResponse]:
        return self.repository.get_all_game_info()

    def catalog_filter_sort(
        self, game_info_filter_sort_dto: FilterSortGameInfoDTORequest
    ) -> list[GameInfoDTOResponse]:
        return self.repository.catalog_filter_sort(game_info_filter_sort_dto)

    def set_like_game_info_by_uuid(
        self, game_info_uuid: UUID, player_uuid: UUID
    ) -> GameInfoDTOResponse:
        return self.repository.set_like_game_info_by_uuid(game_info_uuid, player_uuid)
