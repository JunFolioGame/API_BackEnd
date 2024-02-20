from typing import List
from uuid import UUID

from additional_service.services_interfaces import AdditionalServiceInterface
from catalog.dto import CreateGameInfoDTO, GameInfoDTOResponse, UpdateGameInfoDTORequest
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

    def create_game_info(
        self, game_info_dto: CreateGameInfoDTO, bytesio_file
    ) -> GameInfoDTOResponse:
        """Create new game_info"""
        if bytesio_file:
            image_path = self.additional_service.upload_file_to_s3(
                group_name="game_info",
                object_name=game_info_dto.name_en,
                bytesio_file=bytesio_file,
            )
            game_info_dto.photo = image_path
        return self.game_info_service.create_game_info(game_info_dto)

    def get_game_info_by_uuid(self, uuid: UUID) -> GameInfoDTOResponse:
        return self.game_info_service.get_game_info_by_uuid(uuid)

    def update_game_info_by_uuid(
        self, game_info_to_update: UpdateGameInfoDTORequest, bytesio_file
    ) -> GameInfoDTOResponse:
        if bytesio_file:
            image_path = self.additional_service.upload_file_to_s3(
                group_name="game_info",
                object_name=game_info_to_update.name_en
                or game_info_to_update.uuid.__str__(),
                bytesio_file=bytesio_file,
            )
            game_info_to_update.photo = image_path
        return self.game_info_service.update_game_info_by_uuid(game_info_to_update)

    def delete_game_info_by_uuid(self, uuid: UUID) -> dict:
        result_of_delete_operation = self.game_info_service.delete_game_info_by_uuid(
            uuid
        )
        list_photo_url = result_of_delete_operation.get("photo_list", None)
        for photo_url in list_photo_url:
            self.additional_service.delete_file_from_s3(photo_url=photo_url)

        return result_of_delete_operation

    def get_all_game_info(self) -> List[GameInfoDTOResponse]:
        return self.game_info_service.get_all_game_info()
