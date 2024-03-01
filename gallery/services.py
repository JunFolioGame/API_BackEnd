from uuid import UUID
from gallery.dto import GalleryDTO, CreateGalleryDTO
from gallery.services_interfaces import AbstractGalleryServiceInterface
from gallery.repository_interfaces import AbstractGalleryRepositoryInterface


class GalleryService(AbstractGalleryServiceInterface):
    def __init__(self, repository: AbstractGalleryRepositoryInterface):
        self.repository = repository

    def create_gallery(self, gallery: CreateGalleryDTO) -> GalleryDTO:
        return self.repository.create_gallery(gallery=gallery)

    def get_gallery(self, game_uuid: UUID) -> list[GalleryDTO]:
        return self.repository.get_gallery(game_uuid=game_uuid)
