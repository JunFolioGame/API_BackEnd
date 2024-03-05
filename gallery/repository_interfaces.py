from abc import ABCMeta, abstractmethod
from uuid import UUID

from gallery.dto import CreateGalleryDTO, GalleryDTO


class AbstractGalleryRepositoryInterface(metaclass=ABCMeta):
    @abstractmethod
    def create_gallery(self, gallery: CreateGalleryDTO) -> GalleryDTO:
        pass

    @abstractmethod
    def get_gallery(self, game_uuid: UUID) -> list[GalleryDTO]:
        pass

    @abstractmethod
    def set_like_gallery_item_by_uuid(
        self, gallery_uuid: UUID, player_uuid: UUID
    ) -> GalleryDTO:
        pass

    @abstractmethod
    def unset_like_gallery_item_by_uuid(
        self, gallery_uuid: UUID, player_uuid: UUID
    ) -> GalleryDTO:
        pass
