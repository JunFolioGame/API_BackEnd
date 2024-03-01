from abc import abstractmethod, ABCMeta
from uuid import UUID
from gallery.dto import GalleryDTO, CreateGalleryDTO


class AbstractGalleryServiceInterface(metaclass=ABCMeta):
    @abstractmethod
    def create_gallery(self, gallery: CreateGalleryDTO) -> GalleryDTO:
        pass

    @abstractmethod
    def get_gallery(self, game_uuid: UUID) -> list[GalleryDTO]:
        pass
