from django.db import models
from catalog.models import GameInfo
from players.models import Player


class GalleryItem(models.Model):
    """Gallery item for the results"""

    topic = models.CharField(max_length=255, verbose_name="Тема гри")
    photo = models.CharField(max_length=255, verbose_name="Зображення")
    game = models.ForeignKey(GameInfo, on_delete=models.CASCADE, related_name="gallery")
    team = models.ManyToManyField(Player)
    team_name = models.CharField(max_length=255, verbose_name="Назва команди")
