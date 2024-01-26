from uuid import uuid4

from django.db import models


class Developer(models.Model):
    """Developers model ua and en language"""

    developer_uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name_ua = models.CharField(max_length=50, verbose_name="Ім'я")
    name_en = models.CharField(max_length=50, verbose_name="Name")
    role_ua = models.CharField(max_length=50, verbose_name="Роль")
    photo = models.CharField(verbose_name="Фото")
    is_active = models.BooleanField("Активний учасник", default=False)
