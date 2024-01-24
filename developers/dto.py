from uuid import UUID

from pydantic import BaseModel


class CreateDeveloperDTO(BaseModel):
    name_ua: str
    name_en: str
    role_ua: str
    photo: str
    is_active: bool = False


class UpdateDeveloperDTO(CreateDeveloperDTO):
    ...


class DeveloperDTO(CreateDeveloperDTO):
    developer_uuid: UUID
