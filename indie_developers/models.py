from django.contrib.auth.models import AbstractUser
from django.db import models


class DeveloperUser(AbstractUser):
    game_server_url = models.URLField(null=True, blank=True)
