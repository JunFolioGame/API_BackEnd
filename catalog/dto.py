from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CreateGameInfoDTO(BaseModel):
    name_ua: str
    name_en: str
    photo: str = ""
    description_ua: str
    description_en: str
    is_team: bool = False
    is_active: bool = False
    members: int = 0


class GameInfoDTOResponse(CreateGameInfoDTO):
    uuid: UUID
    like__number: int
    is_active: bool


class UpdateGameInfoDTORequest(GameInfoDTOResponse):
    name_ua: Optional[str] = None
    name_en: Optional[str] = None
    description_ua: Optional[str] = None
    description_en: Optional[str] = None
    members: Optional[int] = None
    role_ua: Optional[str] = None
    like__number: Optional[int] = None
    photo: Optional[str] = None
    is_active: Optional[bool] = None
    is_team: Optional[bool] = None

