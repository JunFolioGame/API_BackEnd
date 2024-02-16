from rest_framework import serializers


class UpdatePlayerDTOSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
