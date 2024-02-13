from django.core.exceptions import ValidationError


class DeveloperDoesNotExist(ValidationError):
    def __init__(self):
        super().__init__("Developer doesn't exist")