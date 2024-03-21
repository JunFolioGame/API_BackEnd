import random
import string

from django.db import models

from players.models import Player


def identificator_generator() -> str:
    characters = string.ascii_uppercase + string.digits
    return "".join(random.choice(characters) for _ in range(6))


class GameSession(models.Model):
    """Developers model ua and en language"""

    identificator = models.CharField(
        max_length=6,
        primary_key=True,
        default=identificator_generator,
        verbose_name="Ідентифікатор",
    )
    is_active = models.BooleanField(default=True)
    final_teams = models.SmallIntegerField(
        null=True,
        verbose_name="Фінальна кількість команд",
    )
    creator = models.ForeignKey(
        Player, related_name="game", on_delete=models.SET_NULL, null=True
    )
    team_min = models.SmallIntegerField(verbose_name="Мінімальна кількість команд")
    team_max = models.SmallIntegerField(verbose_name="Максимальна кількість команд")
    team_players_min = models.SmallIntegerField(
        verbose_name="Мінімальна кількість гравців у одній команді"
    )
    team_players_max = models.SmallIntegerField(
        verbose_name="Максимальна кількість гравців у одній команді"
    )
    lobby = models.ManyToManyField(Player, verbose_name="Доєднані гравці", blank=True)
