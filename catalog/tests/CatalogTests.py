import os

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase

from catalog.dto import CreateGameInfoDTO
from catalog.repositories import GameInfoRepository


class CatalogTests(APITestCase):
    def setUp(self):
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

        repository = GameInfoRepository()
        game_info = repository.create_game_info(
            CreateGameInfoDTO(
                name_ua="Test Name UA",
                name_en="Test Name EN",
                photo="test.jpg",
                description_ua="Test Description UA",
                description_en="Test Description EN",
                is_team=False,
                members=10,
            )
        )
        self.game_info_uuid = game_info.uuid

    # Positive test case for APICreateGameInfoView post method
    def test_create_game_info_success(self):
        data = {
            "name_ua": "Test Name UA 2",
            "name_en": "Test Name EN 2",
            "photo_jpeg": self.photo_jpeg,
            "description_ua": "Test Description UA 2",
            "description_en": "Test Description EN 2",
            "is_team": False,
            "members": 10,
        }
        response = self.client.post("/api/v1/game_info/", data=data)
        assert response.status_code == 201
        assert response.data["status"] == "success"
        assert response.data["message"] == "Successful game_info creation"

    # Negative test case for APICreateGameInfoView post method
    def test_create_game_info_failure_invalid_data(self):
        data = {
            "name_ua": 1,
            "name_en": "Test Name EN",
            "description_ua": "Test Description UA 2",
            "description_en": "Test Description EN 2",
            "is_team": False,
            "members": 10,
        }
        response = self.client.post("/api/v1/game_info/", data=data)
        assert response.status_code == 400

    # Positive test case for ApiGameInfoView get method
    def test_get_game_info_success(self):
        uuid = self.game_info_uuid
        response = self.client.get(f"/api/v1/game_info/{uuid}/")
        assert response.status_code == 200
        assert response.data["status"] == "success"
        assert response.data["message"] == "Successful get game_info information"

    # Negative test case for ApiGameInfoView get method
    def test_get_game_info_failure_not_found(self):
        uuid = "invalid-uuid"
        response = self.client.get(f"/api/v1/game_info/{uuid}/")
        assert response.status_code == 404

    # Positive test case for ApiGameInfoView put method
    def test_update_game_info_success(self):
        uuid = self.game_info_uuid
        data = {
            "name_ua": "Updated Name UA",
            "name_en": "Updated Name EN",
            "photo_jpeg": self.photo_jpeg,
            "description_ua": "Updated Description UA",
            "description_en": "Updated Description EN",
            "is_team": True,
            "members": 20,
        }
        response = self.client.put(f"/api/v1/game_info/{uuid}/", data=data)
        assert response.status_code == 200
        assert response.data["status"] == "success"
        assert response.data["message"] == "Successful update game_info information"

    # Negative test case for ApiGameInfoView put method
    def test_update_game_info_failure_not_found(self):
        uuid = "invalid-uuid"
        data = {
            "name_ua": "Updated Name UA",
            "name_en": "Updated Name EN",
            "description_ua": "Updated Description UA",
            "description_en": "Updated Description EN",
            "is_team": True,
            "members": 20,
        }
        response = self.client.put(f"/api/v1/game_info/{uuid}/", data=data)
        assert response.status_code == 404

    # Positive test case for ApiGameInfoView delete method
    def test_delete_game_info_success(self):
        uuid = self.game_info_uuid
        response = self.client.delete(f"/api/v1/game_info/{uuid}/")
        assert response.status_code == 200
        assert response.data["status"] == "success"
        assert response.data["message"] == "Successful delete game_info."

    # Negative test case for ApiGameInfoView delete method
    def test_delete_game_info_failure_not_found(self):
        uuid = "invalid-uuid"
        response = self.client.delete(f"/api/v1/game_info/{uuid}/")
        assert response.status_code == 404

    # Positive test case for APIAllGameInfoView get method
    def test_get_all_game_info_success(self):
        response = self.client.get("/api/v1/game_info/all/")
        assert response.status_code == 200
        assert response.data["status"] == "success"
        assert response.data["message"] == "Successful get list of all game_infos"
