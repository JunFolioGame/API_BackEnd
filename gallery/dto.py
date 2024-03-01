from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class GalleryDTO(BaseModel):
    topic: str
    photo: str
    team_name: str


class CreateGalleryDTO(GalleryDTO):
    photo: Optional[str] = None
    game: UUID
