from rest_framework import serializers


class CreateGameSessionDTOSerializer(serializers.Serializer):
    team_min = serializers.IntegerField()
    team_max = serializers.IntegerField()
    team_players_min = serializers.IntegerField()
    team_players_max = serializers.IntegerField()
