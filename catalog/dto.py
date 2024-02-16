from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CreateGameInfoDTO(BaseModel):
    name_ua: str
    name_en: str
    photo: str
    description_ua: str
    description_en: str
    is_team: bool = False
    is_active: bool = False
    members: int = 0


class GameInfoDTO(CreateGameInfoDTO):
    game_info_uuid: UUID
    stat: UUID
    is_active: bool


class UpdateGameInfoDTO(GameInfoDTO):
    name_ua: Optional[str] = None
    name_en: Optional[str] = None
    description_ua: str
    description_en: str
    members: int = 0
    role_ua: Optional[str] = None
    photo: Optional[str] = None
    is_active: Optional[bool] = None
    is_team: Optional[bool] = None

