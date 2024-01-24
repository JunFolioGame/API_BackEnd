from rest_framework import serializers


class CreateUpdateDeveloperDTOSerializer(serializers.Serializer):
    name_ua = serializers.CharField(max_length=50)
    name_en = serializers.CharField(max_length=50)
    role_ua = serializers.CharField(max_length=50)
    photo = serializers.CharField(max_length=50)
    is_active = serializers.BooleanField()

    def create(self, validated_data):
        raise NotImplementedError("Method not implemented")

    def update(self, instance, validated_data):
        raise NotImplementedError("Method not implemented")
