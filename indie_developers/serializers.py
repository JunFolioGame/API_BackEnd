from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class DeveloperRegistrationSerializer(UserCreateSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    game_server_url = serializers.URLField(required=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'password', 'game_server_url')


class DeveloperSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'game_server_url')
