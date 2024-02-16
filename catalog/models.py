from uuid import uuid4

from django.db import models


class CoreModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    create_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="created"
    )
    update_at = models.DateTimeField(auto_now=True, verbose_name="updated")

    class Meta:
        abstract = True


class Like(CoreModel):
    stat = models.IntegerField(default=0, verbose_name="Популярність")
    list_vote_user_id = models.IntegerField(  # models.ManyToManyField(
        default=0,
        #     "users.User",
        #     unique=True,
        verbose_name="Список користувачів",
        related_name="like_list_vote_user_id",
    )

    def __str__(self):
        return f"id: {self.uuid} likes: {self.stat}"


class GameInfo(CoreModel):
    """GameInfo model ua and en language"""

    name_ua = models.TextField("Назва ua", max_length=50, unique=True)
    name_en = models.TextField("Назва en", max_length=50, unique=True)
    photo = models.CharField(max_length=255, verbose_name="Зображння")
    description_ua = models.TextField("Опис ua")
    description_en = models.TextField("Опис en")
    is_team = models.BooleanField("Командна", default=False)
    is_active = models.BooleanField("Активна", default=False)
    stat = models.OneToOneField(
        Like, on_delete=models.CASCADE, verbose_name="Популярність"
    )
    members = models.IntegerField("Кількість учасників", default=0)

    def __str__(self):
        return self.name_ua

    class Meta:
        verbose_name = "Інформація про гру"
        verbose_name_plural = "Інформація про Ігри"
