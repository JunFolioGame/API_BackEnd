from django.core.exceptions import ValidationError


class GameSessionDoesNotExist(ValidationError):
    def __init__(self):
        super().__init__("GameSession doesn't exist")


class GameSessionFull(ValidationError):
    def __init__(self):
        super().__init__("GameSession full of players")


class GameSessionNotEnough(ValidationError):
    def __init__(self):
        super().__init__("GameSession not enough players")
