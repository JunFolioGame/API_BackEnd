from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class CreateDeveloperDTOSerializer(serializers.Serializer):
    name_ua = serializers.CharField(max_length=50)
    name_en = serializers.CharField(max_length=50)
    role_ua = serializers.CharField(max_length=50)
    photo = serializers.CharField()
    photo_jpeg = serializers.ImageField()
    is_active = serializers.BooleanField()

    def validate_photo_jpeg(self, value):
        # перевірка розміру файлу
        max_size = 10 * 1024 * 1024  # 10 МБ (змініть за потребою)
        if value and value.size > max_size:
            raise ValidationError(
                f"Розмір файлу перевищує максимально допустимий розмір {max_size} байт."
            )

        return value

    def create(self, validated_data):
        raise NotImplementedError("Method not implemented")

    def update(self, instance, validated_data):
        raise NotImplementedError("Method not implemented")


class UpdateDeveloperDTOSerializer(CreateDeveloperDTOSerializer):
    name_ua = serializers.CharField(max_length=50, required=False, allow_null=True)
    name_en = serializers.CharField(max_length=50, required=False, allow_null=True)
    role_ua = serializers.CharField(max_length=50, required=False, allow_null=True)
    photo = serializers.CharField(max_length=50, required=False, allow_null=True)
    photo_jpeg = serializers.ImageField(required=False, allow_null=True)
    is_active = serializers.BooleanField(required=False, allow_null=True, default=None)
