from uuid import UUID

from pydantic import BaseModel


class CreatePlayerDTO(BaseModel):
    api_adress: str
    browser_info: str


class PlayerDTO(CreatePlayerDTO):
    player_uuid: UUID
    username: str
