import os
from uuid import uuid4

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from developers.dto import CreateDeveloperDTO
from developers.repositories import DeveloperRepository


class DevelopersTests(APITestCase):

    def setUp(self):

        self.url = reverse("api:developers:developers")

        with open(os.path.join(os.path.dirname(__file__), "sample_photo.jpg"), "rb") as photo_file:
            self.photo_jpeg = SimpleUploadedFile(
                "sample_photo.jpg", photo_file.read(), content_type="image/jpeg"
            )

        with open(
            os.path.join(os.path.dirname(__file__), "wrong_sample_photo.jpg"), "rb"
        ) as photo_file:
            self.wrong_photo_jpeg = SimpleUploadedFile(
                "wrong_sample_photo.jpg", photo_file.read(), content_type="image/jpeg"
            )

        repository = DeveloperRepository()
        developer = repository.create_developer(
            CreateDeveloperDTO(
                name_ua="тест_1",
                name_en="test_1",
                role_ua="Користувач",
                photo="Фото",
                is_active="True",
            )
        )
        self.developer_uuid = developer.developer_uuid

    # -------------------------------------LIST DEVELOPERS------------------------------------------

    def test_developer_list_success(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(len(data["data"]), 1)
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful get list of all developers")

        user = data["data"][0]
        self.assertEqual(user["name_ua"], "тест_1")
        self.assertEqual(user["name_en"], "test_1")
        self.assertEqual(user["role_ua"], "Користувач")
        self.assertEqual(user["photo"], "Фото")
        self.assertEqual(user["is_active"], True)
        self.assertEqual(user["developer_uuid"], self.developer_uuid)

    # -------------------------------------RETRIEVE DEVELOPER---------------------------------------

    def test_developer_retrieve_wrong_not_found(self):

        while True:
            random_uuid = uuid4()
            if random_uuid != self.developer_uuid:
                break

        response = self.client.get(self.url + str(random_uuid))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        data = response.data
        self.assertEqual(data["status"], "failed")
        self.assertEqual(data["message"], "Developer doesn't exist")

    def test_developer_retrieve_success(self):

        response = self.client.get(self.url + str(self.developer_uuid))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful get developer information")
        user = data["data"]
        self.assertEqual(user["name_ua"], "тест_1")
        self.assertEqual(user["name_en"], "test_1")
        self.assertEqual(user["role_ua"], "Користувач")
        self.assertEqual(user["photo"], "Фото")
        self.assertEqual(user["is_active"], True)
        self.assertEqual(user["developer_uuid"], self.developer_uuid)

    # --------------------------------------DESTROY DEVELOPER---------------------------------------

    def test_developer_destroy_wrong_not_found(self):

        while True:
            random_uuid = uuid4()
            if random_uuid != self.developer_uuid:
                break

        response = self.client.delete(self.url + str(random_uuid))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        data = response.data
        self.assertEqual(data["status"], "failed")
        self.assertEqual(data["message"], "Developer doesn't exist")

    def test_developer_destroy_success(self):

        response = self.client.delete(self.url + str(self.developer_uuid))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful delete developer.")
        self.assertEqual(data["data"], None)

    # --------------------------------------UPDATE DEVELOPER----------------------------------------

    def test_developer_update_wrong_not_found(self):

        while True:
            random_uuid = uuid4()
            if random_uuid != self.developer_uuid:
                break

        response = self.client.put(self.url + str(random_uuid))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        data = response.data
        self.assertEqual(data["status"], "failed")
        self.assertEqual(data["message"], "Developer doesn't exist")

    def test_developer_update_wrong_bad_photo(self):

        update_data = {"photo_jpeg": self.wrong_photo_jpeg}
        response = self.client.put(self.url + str(self.developer_uuid), data=update_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.data
        self.assertEqual(data["status"], "failed")

        # Треба якусь нормальну помилку для завеликого файлу зробити а не строку
        self.assertEqual(
            data["message"],
            "{'photo_jpeg': [ErrorDetail(string='Розмір файлу перевищує максимально допустимий розмір 10485760 байт.', code='invalid')]}",
        )

    def test_developer_update_photo_success(self):

        update_data = {"photo_jpeg": self.photo_jpeg}
        response = self.client.put(self.url + str(self.developer_uuid), data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful update developer information")

        user = data["data"]
        self.assertEqual(user["name_ua"], "тест_1")
        self.assertEqual(user["name_en"], "test_1")
        self.assertEqual(user["role_ua"], "Користувач")
        self.assertEqual(user["is_active"], True)
        self.assertEqual(user["developer_uuid"], self.developer_uuid)

    def test_developer_update_empty_success(self):

        update_data = {}
        response = self.client.put(self.url + str(self.developer_uuid), data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful update developer information")

        user = data["data"]
        self.assertEqual(user["name_ua"], "тест_1")
        self.assertEqual(user["name_en"], "test_1")
        self.assertEqual(user["role_ua"], "Користувач")
        self.assertEqual(user["photo"], "Фото")
        self.assertEqual(user["is_active"], True)
        self.assertEqual(user["developer_uuid"], self.developer_uuid)

    def test_developer_update_name_ua_success(self):

        update_data = {
            "name_ua": "Петро",
        }
        response = self.client.put(self.url + str(self.developer_uuid), data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful update developer information")

        user = data["data"]
        self.assertEqual(user["name_ua"], "Петро")
        self.assertEqual(user["name_en"], "test_1")
        self.assertEqual(user["role_ua"], "Користувач")
        self.assertEqual(user["photo"], "Фото")
        self.assertEqual(user["is_active"], True)
        self.assertEqual(user["developer_uuid"], self.developer_uuid)

    def test_developer_update_name_en_success(self):

        update_data = {
            "name_en": "Petro",
        }
        response = self.client.put(self.url + str(self.developer_uuid), data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful update developer information")

        user = data["data"]
        self.assertEqual(user["name_ua"], "тест_1")
        self.assertEqual(user["name_en"], "Petro")
        self.assertEqual(user["role_ua"], "Користувач")
        self.assertEqual(user["photo"], "Фото")
        self.assertEqual(user["is_active"], True)
        self.assertEqual(user["developer_uuid"], self.developer_uuid)

    def test_developer_update_role_ua_success(self):

        update_data = {
            "role_ua": "Власник",
        }
        response = self.client.put(self.url + str(self.developer_uuid), data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful update developer information")

        user = data["data"]
        self.assertEqual(user["name_ua"], "тест_1")
        self.assertEqual(user["name_en"], "test_1")
        self.assertEqual(user["role_ua"], "Власник")
        self.assertEqual(user["photo"], "Фото")
        self.assertEqual(user["is_active"], True)
        self.assertEqual(user["developer_uuid"], self.developer_uuid)

    def test_developer_update_photo_success(self):

        update_data = {
            "photo": "Фото 2",
        }
        response = self.client.put(self.url + str(self.developer_uuid), data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful update developer information")

        user = data["data"]
        self.assertEqual(user["name_ua"], "тест_1")
        self.assertEqual(user["name_en"], "test_1")
        self.assertEqual(user["role_ua"], "Користувач")
        self.assertEqual(user["photo"], "Фото 2")
        self.assertEqual(user["is_active"], True)
        self.assertEqual(user["developer_uuid"], self.developer_uuid)

    def test_developer_update_is_active_success(self):

        update_data = {
            "is_active": False,
        }
        response = self.client.put(self.url + str(self.developer_uuid), data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful update developer information")

        user = data["data"]
        self.assertEqual(user["name_ua"], "тест_1")
        self.assertEqual(user["name_en"], "test_1")
        self.assertEqual(user["role_ua"], "Користувач")
        self.assertEqual(user["photo"], "Фото")
        self.assertEqual(user["is_active"], False)
        self.assertEqual(user["developer_uuid"], self.developer_uuid)

    def test_developer_update_change_all_success(self):

        update_data = {
            "name_ua": "Петро",
            "name_en": "Petro",
            "role_ua": "Власник",
            "photo": "Фото 2",
            "is_active": False,
        }
        response = self.client.put(self.url + str(self.developer_uuid), data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful update developer information")

        user = data["data"]
        self.assertEqual(user["name_ua"], "Петро")
        self.assertEqual(user["name_en"], "Petro")
        self.assertEqual(user["role_ua"], "Власник")
        self.assertEqual(user["photo"], "Фото 2")
        self.assertEqual(user["is_active"], False)
        self.assertEqual(user["developer_uuid"], self.developer_uuid)

    # --------------------------------------CREATE DEVELOPER----------------------------------------

    # Для всіх required треба якусь нормальну помилку зробити а не строку
    def test_developer_create_wrong_empty(self):

        create_data = {}
        response = self.client.post(self.url, data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")

    def test_developer_create_wrong_name_ua_required(self):

        create_data = {
            "name_en": "test_2",
            "role_ua": "Власник",
            "photo_jpeg": self.photo_jpeg,
            "is_active": True,
        }

        response = self.client.post(self.url, data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")
        self.assertEqual(
            response.data["message"],
            "{'name_ua': [ErrorDetail(string='This field is required.', code='required')]}",
        )

    def test_developer_create_wrong_name_en_required(self):

        create_data = {
            "name_ua": "тест_2",
            "role_ua": "Власник",
            "photo_jpeg": self.photo_jpeg,
            "is_active": True,
        }

        response = self.client.post(self.url, data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")
        self.assertEqual(
            response.data["message"],
            "{'name_en': [ErrorDetail(string='This field is required.', code='required')]}",
        )

    def test_developer_create_wrong_role_ua_required(self):

        create_data = {
            "name_ua": "тест_2",
            "name_en": "test_2",
            "photo_jpeg": self.photo_jpeg,
            "is_active": True,
        }

        response = self.client.post(self.url, data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")
        self.assertEqual(
            response.data["message"],
            "{'role_ua': [ErrorDetail(string='This field is required.', code='required')]}",
        )

    def test_developer_create_wrong_photo_jpeg_required(self):

        create_data = {
            "name_ua": "тест_2",
            "name_en": "test_2",
            "role_ua": "Власник",
            "is_active": True,
        }

        response = self.client.post(self.url, data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")
        self.assertEqual(
            response.data["message"],
            "{'photo_jpeg': [ErrorDetail(string='No file was submitted.', code='required')]}",
        )

    def test_developer_create_wrong_bad_photo(self):

        create_data = {
            "name_ua": "тест_2",
            "name_en": "test_2",
            "role_ua": "Власник",
            "photo_jpeg": self.wrong_photo_jpeg,
            "is_active": True,
        }
        response = self.client.post(self.url, data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.data
        self.assertEqual(data["status"], "failed")
        self.assertEqual(
            data["message"],
            "{'photo_jpeg': [ErrorDetail(string='Розмір файлу перевищує максимально допустимий розмір 10485760 байт.', code='invalid')]}",
        )

    def test_developer_create_success(self):

        create_data = {
            "name_ua": "тест_2",
            "name_en": "test_2",
            "role_ua": "Власник",
            "photo_jpeg": self.photo_jpeg,
        }
        response = self.client.post(self.url, data=create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful developer's creation")

        user = data["data"]
        self.assertEqual(user["name_ua"], "тест_2")
        self.assertEqual(user["name_en"], "test_2")
        self.assertEqual(user["role_ua"], "Власник")
        self.assertEqual(user["is_active"], False)
        # Видаляємо фото, щоб не засмічувати пам'ять
        self.client.delete(self.url + str(user["developer_uuid"]))
