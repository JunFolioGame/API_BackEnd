from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class CreateGameInfoDTOSerializer(serializers.Serializer):
    name_ua = serializers.CharField(max_length=50)
    name_en = serializers.CharField(max_length=50)
    description_ua = serializers.CharField(max_length=255)
    description_en = serializers.CharField(max_length=255)
    members = serializers.IntegerField()
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


class FilterGameInfoDTOSerializer(CreateGameInfoDTOSerializer):
    name_ua = serializers.CharField(max_length=50, required=False, allow_null=True)
    name_en = serializers.CharField(max_length=50, required=False, allow_null=True)
    description_ua = serializers.CharField(
        max_length=50, required=False, allow_null=True
    )
    description_en = serializers.CharField(
        max_length=50, required=False, allow_null=True
    )
    members = serializers.IntegerField(required=False, allow_null=True)
    photo = serializers.CharField(required=False, allow_null=True)
    photo_jpeg = serializers.HiddenField(required=False, allow_null=True, default=None)
    is_team = serializers.BooleanField(required=False, allow_null=True, default=None)
    is_active = serializers.BooleanField(required=False, allow_null=True, default=None)


class UpdateGameInfoDTOSerializer(FilterGameInfoDTOSerializer):
    photo_jpeg = serializers.ImageField(required=False, allow_null=True)


class FilterAndSortGameInfoDTOSerializer(FilterGameInfoDTOSerializer):
    sort_selection = serializers.ChoiceField(
        choices=["popularity", "newness", "member"],
        required=False,
        default="popularity",
    )
    group_or_individual = serializers.ChoiceField(
        choices=["group", "individual"], required=False
    )

    def validate_sort_selection(self, value):
        match value:
            case "popularity":
                return "-like__number"
            case "newness":
                return "-create_at"
            case "member":
                return "-members"
            case _:
                raise ValidationError(f"Невідомий тип сортування: {value}")
