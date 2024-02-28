from typing import List
from uuid import UUID

from additional_service.services_interfaces import AdditionalServiceInterface
from developers.dto import CreateDeveloperDTO, DeveloperDTO, UpdateDeveloperDTO
from developers.services_interfaces import DeveloperServiceInterface


class DeveloperInteractor:
    """Interactor for managing developer"""

    def __init__(
        self,
        developer_service: DeveloperServiceInterface,
        additional_service: AdditionalServiceInterface,
    ):
        self.developer_service = developer_service
        self.additional_service = additional_service

    def create_developer(
        self, developer_dto: CreateDeveloperDTO, bytesio_file
    ) -> DeveloperDTO:
        """Create new developer"""
        if bytesio_file:
            image_path = self.additional_service.upload_file_to_s3(
                group_name="developers",
                object_name=developer_dto.name_en,
                bytesio_file=bytesio_file,
            )
            developer_dto.photo = image_path
        return self.developer_service.create_developer(developer_dto)

    def get_developer_by_uuid(self, developer_uuid: UUID) -> DeveloperDTO:
        return self.developer_service.get_developer_by_uuid(developer_uuid)

    def update_developer_by_uuid(
        self, developer_to_update: UpdateDeveloperDTO, bytesio_file
    ) -> DeveloperDTO:
        if bytesio_file:
            image_path = self.additional_service.upload_file_to_s3(
                group_name="developers",
                object_name=developer_to_update.name_en
                or developer_to_update.developer_uuid.__str__(),
                bytesio_file=bytesio_file,
            )
            developer_to_update.photo = image_path
        return self.developer_service.update_developer_by_uuid(developer_to_update)

    def delete_developer_by_uuid(self, developer_uuid: UUID) -> None:
        photo_url = self.get_developer_by_uuid(developer_uuid=developer_uuid).photo
        self.additional_service.delete_file_from_s3(photo_url=photo_url)
        return self.developer_service.delete_developer_by_uuid(developer_uuid)

    def get_all_developers(self) -> List[DeveloperDTO]:
        return self.developer_service.get_all_developers()
