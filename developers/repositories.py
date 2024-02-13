from uuid import UUID

from annoying.functions import get_object_or_None

from developers.dto import DeveloperDTO, UpdateDeveloperDTO, CreateDeveloperDTO
from developers.exceptions import DeveloperDoesNotExist
from developers.models import Developer
from developers.repository_interfaces import AbstractDeveloperRepositoryInterface


class DeveloperRepository(AbstractDeveloperRepositoryInterface):
    def create_developer(self, developer: CreateDeveloperDTO) -> DeveloperDTO:
        developer = Developer.objects.create(
            name_ua=developer.name_ua,
            name_en=developer.name_en,
            role_ua=developer.role_ua,
            photo=developer.photo,
            is_active=developer.is_active
        )
        return self._developer_to_dto(developer)

    def get_developer_by_uuid(self, developer_uuid: UUID) -> DeveloperDTO:
        developer = get_object_or_None(Developer, developer_uuid=developer_uuid)
        if not developer:
            raise DeveloperDoesNotExist()
        return self._developer_to_dto(developer)

    def update_developer_by_uuid(
        self, developer_to_update: UpdateDeveloperDTO
    ) -> DeveloperDTO:
        developer = Developer.objects.filter(
            developer_uuid=developer_to_update.developer_uuid
        )
        if not developer:
            raise DeveloperDoesNotExist()
        filtered_param_without_none = {
            k: v for k, v in developer_to_update.model_dump().items() if v is not None
        }
        developer.update(**filtered_param_without_none)
        developer = developer.get()
        return self._developer_to_dto(developer)

    def delete_developer_by_uuid(self, developer_uuid: UUID) -> None:
        developer = get_object_or_None(Developer, developer_uuid=developer_uuid)
        if not developer:
            raise DeveloperDoesNotExist()
        developer.delete()

    def get_all_developers(self) -> list[DeveloperDTO]:
        developers = Developer.objects.all()
        return [self._developer_to_dto(developer) for developer in developers]

    def _developer_to_dto(self, developer: Developer) -> DeveloperDTO:
        return DeveloperDTO(
            developer_uuid=developer.developer_uuid,
            name_ua=developer.name_ua,
            name_en=developer.name_en,
            role_ua=developer.role_ua,
            photo=developer.photo,
            is_active=developer.is_active,
        )
