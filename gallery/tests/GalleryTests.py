import os
from uuid import uuid4

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from catalog.dto import CreateGameInfoDTO
from catalog.repositories import GameInfoRepository
from gallery.dto import CreateGalleryDTO
from gallery.repositories import GalleryRepository


class GalleryTests(APITestCase):
    def setUp(self):
        self.url = reverse("api:gallery:gallery")

        with open(
            os.path.join(os.path.dirname(__file__), "sample_photo.jpg"), "rb"
        ) as photo_file:
            self.photo_jpeg = SimpleUploadedFile(
                "sample_photo.jpg", photo_file.read(), content_type="image/jpeg"
            )

        with open(
            os.path.join(os.path.dirname(__file__), "wrong_sample_photo.jpg"), "rb"
        ) as photo_file:
            self.wrong_photo_jpeg = SimpleUploadedFile(
                "wrong_sample_photo.jpg", photo_file.read(), content_type="image/jpeg"
            )

        game_repository = GameInfoRepository()
        game = game_repository.create_game_info(
            CreateGameInfoDTO(
                name_ua="Ім'я",
                name_en="Name",
                photo="Фото",
                description_ua="Повний опис",
                description_en="Description",
                is_team=True,
                is_active=True,
                members=5,
            )
        )
        self.game_uuid = game.uuid
        gallery_repository = GalleryRepository()
        gallery_repository.create_gallery(
            CreateGalleryDTO(
                topic="Тема", photo="Фото 2", team_name="Команда", game=self.game_uuid
            )
        )

    # -------------------------------------GALLERY LIST---------------------------------
    def test_gallery_list_wrong_invalid_page(self):

        response = self.client.get(self.url + str(self.game_uuid) + "?page=2")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.data
        self.assertEqual(data["detail"], "Invalid page.")

    def test_gallery_list_wrong_not_found(self):

        while True:
            random_uuid = uuid4()
            if random_uuid != self.game_uuid:
                break

        response = self.client.get(self.url + str(random_uuid))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        data = response.data
        self.assertEqual(data["status"], "failed")
        self.assertEqual(data["message"], "GameInfo doesn't exist")

    def test_developer_list_success(self):

        response = self.client.get(self.url + str(self.game_uuid))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(len(data["data"]), 1)
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful get gallery items")

        item = data["data"][0]
        self.assertEqual(item["topic"], "Тема")
        self.assertEqual(item["photo"], "Фото 2")
        self.assertEqual(item["team_name"], "Команда")

    # --------------------------------------CREATE GALLERY------------------------------
    def test_gallery_create_wrong_empty(self):
        create_data = {}
        response = self.client.post(self.url, data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")

    def test_gallery_create_wrong_topic_required(self):
        create_data = {
            "photo_jpeg": self.photo_jpeg,
            "team_name": "Команда 2",
            "game": self.game_uuid,
        }
        response = self.client.post(self.url, data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")

    def test_gallery_create_wrong_photo_jpeg_required(self):
        create_data = {
            "topic": "Тема 2",
            "team_name": "Команда 2",
            "game": self.game_uuid,
        }
        response = self.client.post(self.url, data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")

    def test_gallery_create_wrong_team_name_required(self):
        create_data = {
            "topic": "Тема 2",
            "photo_jpeg": self.photo_jpeg,
            "game": self.game_uuid,
        }
        response = self.client.post(self.url, data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")

    def test_gallery_create_wrong_game_required(self):
        create_data = {
            "topic": "Тема 2",
            "photo_jpeg": self.photo_jpeg,
            "team_name": "Команда 2",
        }
        response = self.client.post(self.url, data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")

    def test_gallery_create_wrong_bad_photo(self):
        create_data = {
            "topic": "Тема 2",
            "photo_jpeg": self.wrong_photo_jpeg,
            "team_name": "Команда 2",
            "game": self.game_uuid,
        }
        response = self.client.post(self.url, data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.data
        self.assertEqual(data["status"], "failed")

    def test_gallery_create_success(self):
        create_data = {
            "topic": "Тема 2",
            "photo_jpeg": self.photo_jpeg,
            "team_name": "Команда 2",
            "game": self.game_uuid,
        }
        response = self.client.post(self.url, data=create_data)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful galery item creation")

        item = data["data"]
        self.assertEqual(item["topic"], "Тема 2")
        self.assertEqual(item["team_name"], "Команда 2")
