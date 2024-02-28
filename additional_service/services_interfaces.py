from abc import ABCMeta, abstractmethod


class AdditionalServiceInterface(metaclass=ABCMeta):
    @abstractmethod
    def upload_file_to_s3(self, group_name: str, object_name: str, bytesio_file) -> str:
        pass

    @abstractmethod
    def delete_file_from_s3(self, photo_url: str) -> None:
        pass
