from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class CreateGameInfoDTOSerializer(serializers.Serializer):
    name_ua = serializers.CharField(max_length=50)
    name_en = serializers.CharField(max_length=50)
    description_ua = serializers.CharField(max_length=50)
    description_en = serializers.CharField(max_length=50)
    photo_jpeg = serializers.ImageField()
    is_team = serializers.BooleanField(required=False, allow_null=True, default=False)
    is_active = serializers.BooleanField(required=False, allow_null=True, default=False)

    def validate_photo_jpeg(self, value):
        # перевірка розміру файлу
        max_size = 10 * 1024 * 1024  # 10 МБ (змініть за потребою)
        if value and value.size > max_size:
            raise ValidationError(
                f"Розмір файлу перевищує максимально допустимий розмір {max_size} байт."
            )

        return value


class UpdateGameInfoDTOSerializer(CreateGameInfoDTOSerializer):
    name_ua = serializers.CharField(max_length=50, required=False, allow_null=True)
    name_en = serializers.CharField(max_length=50, required=False, allow_null=True)
    description_ua = serializers.CharField(
        max_length=50, required=False, allow_null=True
    )
    description_en = serializers.CharField(
        max_length=50, required=False, allow_null=True
    )
    photo = serializers.CharField(required=False, allow_null=True)
    photo_jpeg = serializers.ImageField(required=False, allow_null=True)
