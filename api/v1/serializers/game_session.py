from rest_framework import serializers


class CreateGameSessionDTOSerializer(serializers.Serializer):
    team_min = serializers.IntegerField()
    team_max = serializers.IntegerField()
    team_players_min = serializers.IntegerField()
    team_players_max = serializers.IntegerField()

    def validate(self, attrs):
        for field_name, value in attrs.items():
            if value <= 0:
                raise serializers.ValidationError(
                    {field_name: "Значення повинно бути більше за 0."}
                )
            if value >= 32768:
                raise serializers.ValidationError(
                    {field_name: "Значення повинно бути менше за 32768."}
                )

        team_min = attrs.get("team_min")
        team_max = attrs.get("team_max")
        team_players_min = attrs.get("team_players_min")
        team_players_max = attrs.get("team_players_max")
        if team_max < team_min:
            raise serializers.ValidationError(
                {
                    "team_max": "Максимальна кількість команд повинна бути більшою або \
                        рівною мінімальній кількості команд."
                }
            )

        if team_players_max < team_players_min:
            raise serializers.ValidationError(
                {
                    "team_max": "Максимальна кількість гравці у команді повинна бути \
                        більшою або рівною мінімальній кількості гравців у команді."
                }
            )

        return attrs
