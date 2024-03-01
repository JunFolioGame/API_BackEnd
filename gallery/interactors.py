from gallery.services_interfaces import AbstractGalleryServiceInterface
from additional_service.services_interfaces import AdditionalServiceInterface
from gallery.dto import CreateGalleryDTO, GalleryDTO
from uuid import UUID


class GalleryInteractor:
    def __init__(
        self,
        gallery_service: AbstractGalleryServiceInterface,
        additional_service: AdditionalServiceInterface,
    ):
        self.gallery_service = gallery_service
        self.additional_service = additional_service

    def create_gallery(self, gallery_dto: CreateGalleryDTO, bytesio_file) -> GalleryDTO:
        if bytesio_file:
            image_path = self.additional_service.upload_file_to_s3(
                group_name="gallery",
                object_name=gallery_dto.team_name,
                bytesio_file=bytesio_file,
            )
            gallery_dto.photo = image_path
        return self.gallery_service.create_gallery(gallery=gallery_dto)

    def get_gallery(self, game_uuid: UUID) -> list[GalleryDTO]:
        return self.gallery_service.get_gallery(game_uuid=game_uuid)
