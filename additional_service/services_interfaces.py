from abc import ABCMeta, abstractmethod


class AdditionalServiceInterface(metaclass=ABCMeta):
    @abstractmethod
    def upload_file_to_s3(
        self, group_name: str, object_name: str, bytesio_file
    ) -> None:
        pass
