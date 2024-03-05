from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class CreateGalleryItemDTOSerializer(serializers.Serializer):
    topic = serializers.CharField(max_length=255)
    photo_jpeg = serializers.ImageField()
    team_name = serializers.CharField(max_length=255)

    def validate_photo_jpeg(self, value):
        # перевірка розміру файлу
        max_size = 10 * 1024 * 1024  # 10 МБ (змініть за потребою)
        if value and value.size > max_size:
            raise ValidationError(
                f"Розмір файлу перевищує максимально допустимий розмір {max_size} байт."
            )
        return value
