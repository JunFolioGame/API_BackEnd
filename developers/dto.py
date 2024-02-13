from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CreateDeveloperDTO(BaseModel):
    name_ua: str
    name_en: str
    role_ua: str
    photo: Optional[str] = None
    is_active: bool = False


class DeveloperDTO(CreateDeveloperDTO):
    developer_uuid: UUID
    is_active: bool


class UpdateDeveloperDTO(DeveloperDTO):
    name_ua: Optional[str] = None
    name_en: Optional[str] = None
    role_ua: Optional[str] = None
    photo: Optional[str] = None
    is_active: Optional[bool] = None
