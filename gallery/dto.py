from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class GalleryDTO(BaseModel):
    topic: str
    photo: str
    team_name: str
    gallery_uuid: UUID
    likes: int


class CreateGalleryDTO(GalleryDTO):
    gallery_uuid: Optional[UUID] = None
    photo: Optional[str] = None
    likes: Optional[int] = None
    game: UUID
