from django.core.exceptions import ValidationError


class GalleryItemDoesNotExist(ValidationError):
    def __init__(self):
        super().__init__("GalleryItem doesn't exist")
