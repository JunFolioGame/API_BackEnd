from abc import abstractmethod, ABCMeta
from uuid import UUID

from developers.dto import DeveloperDTO, UpdateDeveloperDTO, CreateDeveloperDTO


class DeveloperServiceInterface(metaclass=ABCMeta):
    @abstractmethod
    def create_developer(self, developer_dto: CreateDeveloperDTO) -> DeveloperDTO:
        pass

    @abstractmethod
    def get_developer_by_uuid(self, developer_uuid: UUID) -> DeveloperDTO:
        pass

    @abstractmethod
    def update_developer_by_uuid(
        self, developer_to_update: UpdateDeveloperDTO
    ) -> DeveloperDTO:
        pass

    @abstractmethod
    def delete_developer_by_uuid(self, developer_uuid: UUID) -> None:
        pass

    @abstractmethod
    def get_all_developers(self) -> list[DeveloperDTO]:
        pass
