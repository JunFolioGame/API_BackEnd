from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class GameSessionDTO(BaseModel):
    session_identificator: str
    team_min: int
    team_max: int
    team_players_min: int
    team_players_max: int
    lobby: Optional[List[UUID] | List[List[UUID]]] = []


class CreateGameSessionDTO(GameSessionDTO):
    creator_uuid: UUID
    session_identificator: Optional[str] = ""
