from django.core.exceptions import ValidationError


class PlayerDoesNotExist(ValidationError):
    def __init__(self):
        super().__init__("Player doesn't exist")


class WrongUUID(ValidationError):
    def __init__(self, value):
        super().__init__(f"{value} is not a valid UUID")
