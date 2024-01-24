from typing import List
from uuid import UUID

from developers.dto import CreateDeveloperDTO, DeveloperDTO, UpdateDeveloperDTO
from developers.services_interfaces import DeveloperServiceInterface


class DeveloperInteractor:
    """Interactor for managing developer"""

    def __init__(
        self,
        developer_service: DeveloperServiceInterface,
    ):
        self.developer_service = developer_service

    def create_developer(self, developer_dto: CreateDeveloperDTO) -> DeveloperDTO:
        """Create new developer"""
        return self.developer_service.create_developer(developer_dto)

    def get_developer_by_uuid(self, developer_uuid: UUID) -> DeveloperDTO:
        return self.developer_service.get_developer_by_uuid(developer_uuid)

    def update_developer_by_uuid(
        self, developer_to_update: UpdateDeveloperDTO
    ) -> DeveloperDTO:
        return self.developer_service.update_developer_by_uuid(developer_to_update)

    def delete_developer_by_uuid(self, developer_uuid: UUID) -> None:
        return self.developer_service.delete_developer_by_uuid(developer_uuid)

    def get_all_developers(self) -> List[DeveloperDTO]:
        return self.developer_service.get_all_developers()
