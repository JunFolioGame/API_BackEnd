from uuid import uuid4

from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from catalog.models import GameInfo
from players.models import Player


class GalleryItem(models.Model):
    """Gallery item for the results"""

    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    text = models.TextField()
    topic = models.CharField(max_length=255, verbose_name="Тема гри")
    photo = models.CharField(max_length=255, verbose_name="Зображення")
    game = models.ForeignKey(GameInfo, on_delete=models.CASCADE, related_name="gallery")
    team_name = models.CharField(max_length=255, verbose_name="Назва команди")


class Vote(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    galleryitem = models.OneToOneField(
        GalleryItem, on_delete=models.CASCADE, verbose_name="Карточка галереї"
    )
    number = models.IntegerField(default=0, verbose_name="Популярність")
    list_like_user_uuid = models.ManyToManyField(
        Player,
        verbose_name="Список користувачів",
    )

    def __str__(self):
        return f"id: {self.uuid} likes: {self.number}"

    def update_number(self):
        self.number = self.list_like_user_uuid.count()
        self.save()


@receiver(m2m_changed, sender=Vote.list_like_user_uuid.through)
def update_like_number(sender, instance, **kwargs):
    instance.update_number()
