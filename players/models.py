from uuid import uuid4

from django.db import models


class Player(models.Model):
    """Player model"""

    player_uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    api_adress = models.CharField(max_length=50, verbose_name="API адреса")
    browser_info = models.CharField(
        max_length=255, verbose_name="Інформація про браузер"
    )
    username = models.CharField(
        max_length=50, default="Player", verbose_name="Ім'я користувача"
    )
