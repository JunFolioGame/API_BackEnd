import os
from uuid import uuid4

from django.core.files.uploadedfile import SimpleUploadedFile
from django.http.cookie import SimpleCookie
from rest_framework import status
from rest_framework.test import APITestCase

from catalog.dto import CreateGameInfoDTO
from catalog.repositories import GameInfoRepository
from gallery.dto import CreateGalleryDTO
from gallery.repositories import GalleryRepository
from players.dto import CreatePlayerDTO
from players.repositories import PlayerRepository


class GalleryTests(APITestCase):
    def setUp(self):
        self.url = "/api/v1/gallery/"
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

        player_repository = PlayerRepository()
        player1 = player_repository.create_player(
            CreatePlayerDTO(api_adress="api adress", browser_info="browser info")
        )
        self.player1_uuid = player1.player_uuid
        player2 = player_repository.create_player(
            CreatePlayerDTO(api_adress="api adress 2", browser_info="browser info 2")
        )
        self.player2_uuid = player2.player_uuid

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
        gallery1 = gallery_repository.create_gallery(
            CreateGalleryDTO(
                topic="Тема", photo="Фото 2", team_name="Команда", game=self.game_uuid
            )
        )
        self.gallery1_uuid = gallery1.gallery_uuid

        gallery2 = gallery_repository.create_gallery(
            CreateGalleryDTO(
                topic="Тема 2",
                photo="Фото 3",
                team_name="Команда 2",
                game=self.game_uuid,
            )
        )
        self.gallery2_uuid = gallery2.gallery_uuid

        gallery_repository.set_like_gallery_item_by_uuid(
            gallery_uuid=gallery2.gallery_uuid, player_uuid=player1.player_uuid
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

        response = self.client.get(
            self.url + str(self.game_uuid),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(len(data["data"]), 2)
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful get gallery items")

        item1 = data["data"][0]
        self.assertEqual(item1["topic"], "Тема 2")
        self.assertEqual(item1["photo"], "Фото 3")
        self.assertEqual(item1["team_name"], "Команда 2")
        self.assertEqual(item1["gallery_uuid"], self.gallery2_uuid)
        self.assertEqual(item1["likes"], 1)

        item2 = data["data"][1]
        self.assertEqual(item2["topic"], "Тема")
        self.assertEqual(item2["photo"], "Фото 2")
        self.assertEqual(item2["team_name"], "Команда")
        self.assertEqual(item2["gallery_uuid"], self.gallery1_uuid)
        self.assertEqual(item2["likes"], 0)

    # --------------------------------------CREATE GALLERY------------------------------
    def test_gallery_create_wrong_empty(self):
        create_data = {}
        response = self.client.post(self.url + str(self.game_uuid), data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")

    def test_gallery_create_wrong_topic_required(self):
        create_data = {
            "photo_jpeg": self.photo_jpeg,
            "team_name": "Команда 2",
        }
        response = self.client.post(self.url + str(self.game_uuid), data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")

    def test_gallery_create_wrong_photo_jpeg_required(self):
        create_data = {
            "topic": "Тема 2",
            "team_name": "Команда 2",
        }
        response = self.client.post(self.url + str(self.game_uuid), data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")

    def test_gallery_create_wrong_team_name_required(self):
        create_data = {
            "topic": "Тема 2",
            "photo_jpeg": self.photo_jpeg,
        }
        response = self.client.post(self.url + str(self.game_uuid), data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")

    def test_gallery_create_wrong_bad_photo(self):
        create_data = {
            "topic": "Тема 2",
            "photo_jpeg": self.wrong_photo_jpeg,
            "team_name": "Команда 2",
        }
        response = self.client.post(self.url + str(self.game_uuid), data=create_data)
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
        response = self.client.post(self.url + str(self.game_uuid), data=create_data)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful galery item creation")

        item = data["data"]
        self.assertEqual(item["topic"], "Тема 2")
        self.assertEqual(item["team_name"], "Команда 2")
        self.assertEqual(item["likes"], 0)

    # -------------------------------------LIKE GALLERY---------------------------------

    def test_gallery_like_wrong_bad_cookies(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": "111"})
        response = self.client.get(self.url + str(self.gallery1_uuid) + "/like")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.data
        self.assertEqual(data["status"], "failed")
        self.assertEqual(data["message"], "['111 is not a valid UUID']")

    def test_gallery_like_wrong_not_found(self):
        while True:
            random_uuid = uuid4()
            if random_uuid != self.gallery1_uuid:
                break

        self.client.cookies = SimpleCookie({"PLAYER_UUID": self.player2_uuid})
        response = self.client.get(self.url + str(random_uuid) + "/like")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        data = response.data
        self.assertEqual(data["status"], "failed")
        self.assertEqual(data["message"], "GalleryItem doesn't exist")

    def test_gallery_like_success(self):

        self.client.cookies = SimpleCookie({"PLAYER_UUID": self.player2_uuid})
        response = self.client.get(self.url + str(self.gallery2_uuid) + "/like")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "Success")
        self.assertEqual(data["message"], "Like was successfully set")

        gallery = data["data"]
        self.assertEqual(gallery["topic"], "Тема 2")
        self.assertEqual(gallery["photo"], "Фото 3")
        self.assertEqual(gallery["team_name"], "Команда 2")
        self.assertEqual(gallery["gallery_uuid"], self.gallery2_uuid)
        self.assertEqual(gallery["likes"], 2)

    # ------------------------------------UNLIKE GALLERY--------------------------------

    def test_gallery_unlike_wrong_bad_cookies(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": "111"})
        response = self.client.get(self.url + str(self.gallery1_uuid) + "/unlike")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.data
        self.assertEqual(data["status"], "failed")
        self.assertEqual(data["message"], "['111 is not a valid UUID']")

    def test_gallery_unlike_wrong_not_found(self):
        while True:
            random_uuid = uuid4()
            if random_uuid != self.gallery1_uuid:
                break

        self.client.cookies = SimpleCookie({"PLAYER_UUID": self.player2_uuid})
        response = self.client.get(self.url + str(random_uuid) + "/unlike")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        data = response.data
        self.assertEqual(data["status"], "failed")
        self.assertEqual(data["message"], "GalleryItem doesn't exist")

    def test_gallery_unlike_success(self):

        self.client.cookies = SimpleCookie({"PLAYER_UUID": self.player1_uuid})
        response = self.client.get(self.url + str(self.gallery2_uuid) + "/unlike")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "Success")
        self.assertEqual(data["message"], "Like was successfully unset")

        gallery = data["data"]
        self.assertEqual(gallery["topic"], "Тема 2")
        self.assertEqual(gallery["photo"], "Фото 3")
        self.assertEqual(gallery["team_name"], "Команда 2")
        self.assertEqual(gallery["gallery_uuid"], self.gallery2_uuid)
        self.assertEqual(gallery["likes"], 0)
