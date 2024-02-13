from uuid import UUID

from developers.dto import DeveloperDTO, CreateDeveloperDTO, UpdateDeveloperDTO
from developers.repository_interfaces import AbstractDeveloperRepositoryInterface
from developers.services_interfaces import DeveloperServiceInterface


class DeveloperService(DeveloperServiceInterface):
    def __init__(self, repository: AbstractDeveloperRepositoryInterface):
        self.repository = repository

    def create_developer(self, developer_dto: CreateDeveloperDTO) -> DeveloperDTO:
        return self.repository.create_developer(developer_dto)

    def get_developer_by_uuid(self, developer_uuid: UUID) -> DeveloperDTO:
        return self.repository.get_developer_by_uuid(developer_uuid)

    def update_developer_by_uuid(
        self, developer_to_update: UpdateDeveloperDTO
    ) -> DeveloperDTO:
        return self.repository.update_developer_by_uuid(developer_to_update)

    def delete_developer_by_uuid(self, developer_uuid: UUID) -> None:
        return self.repository.delete_developer_by_uuid(developer_uuid)

    def get_all_developers(self) -> list[DeveloperDTO]:
        return self.repository.get_all_developers()
