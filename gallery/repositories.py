from uuid import UUID

from annoying.functions import get_object_or_None
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from catalog.exceptions import GameInfoDoesNotExist
from catalog.models import GameInfo
from gallery.dto import CreateGalleryDTO, GalleryDTO
from gallery.exceptions import GalleryItemDoesNotExist
from gallery.models import GalleryItem, Vote
from gallery.repository_interfaces import AbstractGalleryRepositoryInterface
from players.exceptions import PlayerDoesNotExist, WrongUUID


class GalleryRepository(AbstractGalleryRepositoryInterface):
    def create_gallery(self, gallery: CreateGalleryDTO) -> GalleryDTO:
        try:
            gallery_object, _ = GalleryItem.objects.get_or_create(
                topic=gallery.topic,
                photo=gallery.photo,
                team_name=gallery.team_name,
                game=GameInfo(uuid=gallery.game),
            )
            Vote.objects.create(galleryitem=gallery_object)
        except IntegrityError:
            raise GameInfoDoesNotExist()
        return self._gallery_to_dto(gallery=gallery_object)

    def get_gallery(self, game_uuid: UUID) -> list[GalleryDTO]:
        game = get_object_or_None(GameInfo, uuid=game_uuid)
        if not game:
            raise GameInfoDoesNotExist()
        return [
            self._gallery_to_dto(gallery=item)
            for item in game.gallery.all().order_by("-vote__number")
        ]

    def get_gallery_by_uuid(self, gallery_uuid: UUID) -> GalleryDTO:
        gallery = get_object_or_None(GalleryItem, uuid=gallery_uuid)
        if not gallery:
            raise GalleryItemDoesNotExist()
        return self._gallery_to_dto(gallery=gallery)

    def set_like_gallery_item_by_uuid(
        self, gallery_uuid: UUID, player_uuid: UUID
    ) -> GalleryDTO:
        gallery_item = get_object_or_None(GalleryItem, uuid=gallery_uuid)
        if not gallery_item:
            raise GalleryItemDoesNotExist
        try:
            gallery_item.vote.list_like_user_uuid.add(player_uuid)
        except ValidationError:
            raise WrongUUID(value=player_uuid)
        except IntegrityError:
            raise PlayerDoesNotExist
        return self._gallery_to_dto(gallery=gallery_item)

    def unset_like_gallery_item_by_uuid(
        self, gallery_uuid: UUID, player_uuid: UUID
    ) -> GalleryDTO:
        gallery_item = get_object_or_None(GalleryItem, uuid=gallery_uuid)
        if not gallery_item:
            raise GalleryItemDoesNotExist
        try:
            gallery_item.vote.list_like_user_uuid.remove(player_uuid)
        except ValidationError:
            raise WrongUUID(value=player_uuid)
        return self._gallery_to_dto(gallery=gallery_item)

    def _gallery_to_dto(self, gallery: GalleryItem) -> GalleryDTO:
        return GalleryDTO(
            topic=gallery.topic,
            photo=gallery.photo,
            team_name=gallery.team_name,
            gallery_uuid=gallery.uuid,
            likes=gallery.vote.number,
        )
