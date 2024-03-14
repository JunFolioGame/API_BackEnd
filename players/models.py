from uuid import uuid4

from django.db import models


class Player(models.Model):
    """Player model"""

    player_uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(
        max_length=50, default="Player", verbose_name="Ім'я користувача"
    )
