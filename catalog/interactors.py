from typing import List
from uuid import UUID

from additional_service.services_interfaces import AdditionalServiceInterface
from catalog.dto import CreateGameInfoDTO, GameInfoDTO, UpdateGameInfoDTO
from catalog.services_interfaces import GameInfoServiceInterface


class GameInfoInteractor:
    """Interactor for managing game_info"""

    def __init__(
        self,
        game_info_service: GameInfoServiceInterface,
        additional_service: AdditionalServiceInterface,
    ):
        self.game_info_service = game_info_service
        self.additional_service = additional_service

    def create_game_info(self, game_info_dto: CreateGameInfoDTO, bytesio_file) -> GameInfoDTO:
        """Create new game_info"""
        if bytesio_file:
            image_path = self.additional_service.upload_file_to_s3(
                group_name="game_infos",
                object_name=game_info_dto.name_en,
                bytesio_file=bytesio_file,
            )
            game_info_dto.photo = image_path
        return self.game_info_service.create_game_info(game_info_dto)

    def get_game_info_by_uuid(self, game_info_uuid: UUID) -> GameInfoDTO:
        return self.game_info_service.get_game_info_by_uuid(game_info_uuid)

    def update_game_info_by_uuid(
        self, game_info_to_update: UpdateGameInfoDTO, bytesio_file
    ) -> GameInfoDTO:
        if bytesio_file:
            image_path = self.additional_service.upload_file_to_s3(
                group_name="game_infos",
                object_name=game_info_to_update.name_en
                or game_info_to_update.game_info_uuid.__str__(),
                bytesio_file=bytesio_file,
            )
            game_info_to_update.photo = image_path
        return self.game_info_service.update_game_info_by_uuid(game_info_to_update)

    def delete_game_info_by_uuid(self, game_info_uuid: UUID) -> None:
        photo_url = self.get_game_info_by_uuid(game_info_uuid=game_info_uuid).photo
        self.additional_service.delete_file_from_s3(photo_url=photo_url)
        return self.game_info_service.delete_game_info_by_uuid(game_info_uuid)

    def get_all_game_info(self) -> List[GameInfoDTO]:
        return self.game_info_service.get_all_game_info()
