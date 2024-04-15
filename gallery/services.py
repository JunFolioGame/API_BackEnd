from uuid import UUID

from gallery.dto import CreateGalleryDTO, GalleryDTO
from gallery.repository_interfaces import AbstractGalleryRepositoryInterface
from gallery.services_interfaces import AbstractGalleryServiceInterface


class GalleryService(AbstractGalleryServiceInterface):
    def __init__(self, repository: AbstractGalleryRepositoryInterface):
        self.repository = repository

    def create_gallery(self, gallery: CreateGalleryDTO) -> GalleryDTO:
        return self.repository.create_gallery(gallery=gallery)

    def get_gallery(self, game_uuid: UUID) -> list[GalleryDTO]:
        return self.repository.get_gallery(game_uuid=game_uuid)

    def get_gallery_by_uuid(self, gallery_uuid: UUID) -> GalleryDTO:
        return self.repository.get_gallery_by_uuid(gallery_uuid=gallery_uuid)

    def set_like_gallery_item_by_uuid(
        self, gallery_uuid: UUID, player_uuid: UUID
    ) -> GalleryDTO:
        return self.repository.set_like_gallery_item_by_uuid(
            gallery_uuid=gallery_uuid, player_uuid=player_uuid
        )

    def unset_like_gallery_item_by_uuid(
        self, gallery_uuid: UUID, player_uuid: UUID
    ) -> GalleryDTO:
        return self.repository.unset_like_gallery_item_by_uuid(
            gallery_uuid=gallery_uuid, player_uuid=player_uuid
        )
