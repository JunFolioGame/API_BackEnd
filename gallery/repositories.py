from uuid import UUID

from annoying.functions import get_object_or_None
from django.db.utils import IntegrityError

from catalog.exceptions import GameInfoDoesNotExist
from catalog.models import GameInfo
from gallery.dto import CreateGalleryDTO, GalleryDTO
from gallery.models import GalleryItem
from gallery.repository_interfaces import AbstractGalleryRepositoryInterface


class GalleryRepository(AbstractGalleryRepositoryInterface):
    def create_gallery(self, gallery: CreateGalleryDTO) -> GalleryDTO:
        try:
            gallery_object, _ = GalleryItem.objects.get_or_create(
                topic=gallery.topic,
                photo=gallery.photo,
                team_name=gallery.team_name,
                game=GameInfo(uuid=gallery.game),
            )
        except IntegrityError:
            raise GameInfoDoesNotExist()
        return self._gallery_to_dto(gallery=gallery_object)

    def get_gallery(self, game_uuid: UUID) -> list[GalleryDTO]:
        game = get_object_or_None(GameInfo, uuid=game_uuid)
        if not game:
            raise GameInfoDoesNotExist()
        return [self._gallery_to_dto(gallery=item) for item in game.gallery.all()]

    def _gallery_to_dto(self, gallery: GalleryItem) -> GalleryDTO:
        return GalleryDTO(
            topic=gallery.topic, photo=gallery.photo, team_name=gallery.team_name
        )
