from uuid import UUID

from pydantic import BaseModel


class PlayerDTO(BaseModel):
    player_uuid: UUID
    username: str
