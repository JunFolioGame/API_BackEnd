from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class GameSessionDTO(BaseModel):
    session_identificator: str
    team_min: int
    team_max: int
    team_players_min: int
    team_players_max: int
    lobby: Optional[List[dict[str, str]] | List[List[dict[str, str]]]] = []


class CreateGameSessionDTO(GameSessionDTO):
    creator_uuid: UUID
    session_identificator: Optional[str] = ""


class StatisticsSessionDTOResponse(BaseModel):
    played: int
    number_of_teams: int
    number_of_games: int | None = None
