from uuid import uuid4

from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from players.models import Player


class CoreModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    create_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="created"
    )
    update_at = models.DateTimeField(auto_now=True, verbose_name="updated")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        abstract = True


class GameInfo(CoreModel):
    """GameInfo model ua and en language"""

    name_ua = models.TextField("Назва ua", max_length=50, unique=True)
    name_en = models.TextField("Назва en", max_length=50, unique=True)
    photo = models.CharField(max_length=255, verbose_name="Зображння")
    description_ua = models.TextField("Опис ua")
    description_en = models.TextField("Опис en")
    is_team = models.BooleanField("Командна", default=False)
    is_active = models.BooleanField("Активна", default=False)

    members = models.IntegerField("Кількість учасників", default=0)

    def __str__(self):
        return self.name_ua

    class Meta:
        verbose_name = "Інформація про гру"
        verbose_name_plural = "Інформація про Ігри"


class Like(CoreModel):
    gameinfo = models.OneToOneField(
        GameInfo, on_delete=models.CASCADE, verbose_name="карточка гри"
    )
    number = models.IntegerField(default=0, verbose_name="Популярність")
    list_vote_user_id = models.ManyToManyField(
        Player,
        verbose_name="Список користувачів",
    )

    def __str__(self):
        return f"id: {self.uuid} likes: {self.number}"

    def update_number(self):
        self.number = self.list_vote_user_id.count()
        self.save()


@receiver(m2m_changed, sender=Like.list_vote_user_id.through)
def update_like_number(sender, instance, **kwargs):
    instance.update_number()


class Picture(CoreModel):
    # photo = models.ManyToManyField(
    #     GameInfo,
    #     related_name="game_info_picture",
    #     verbose_name="Зображення",
    # )
    url_picture = models.CharField(max_length=255, verbose_name="Зображення")
    type_picture = models.CharField(max_length=255, verbose_name="Тип зображення")

    def __str__(self):
        return f"id: {self.uuid} url: {self.url_picture}"
