from django.core.exceptions import ValidationError


class PlayerDoesNotExist(ValidationError):
    def __init__(self):
        super().__init__("Player doesn't exist")
