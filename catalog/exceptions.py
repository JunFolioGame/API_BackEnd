from django.core.exceptions import ValidationError


class GameInfoDoesNotExist(ValidationError):
    def __init__(self):
        super().__init__("GameInfo doesn't exist")


class NameGameAlreadyExists(ValidationError):
    def __init__(self):
        super().__init__("A game with the same name already exists")
