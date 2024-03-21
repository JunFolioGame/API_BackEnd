import os

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from catalog.dto import CreateGameInfoDTO
from catalog.repositories import GameInfoRepository
from game_session.models import GameSession
from game_session.repositories import GameSessionRepository
from players.models import Player
from catalog.models import GameInfo
from players.repositories import PlayerRepository


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
        self.game_info = repository.create_game_info(
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
        self.game_info_uuid = self.game_info.uuid

        player_repository = PlayerRepository()

        self.players = [player_repository.create_player().player_uuid for _ in range(2)]

        self.game_session_repository = GameSessionRepository()

        self.game_session = GameSession.objects.create(
            creator=Player(player_uuid=self.players[0]),
            final_teams=3,
            team_min=2,
            team_max=4,
            team_players_min=4,
            team_players_max=6,
        )

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
        assert response.data["status"] == "Success"
        assert response.data["message"] == "Successful get list of all game_info"

    def test_get_statistics_on_the_site(self):
        response = self.client.get("/api/v1/game_info/statistic/")
        assert response.status_code == 200
        assert response.data["status"] == "Success"
        assert (
            response.data["message"]
            == "Successful get statistics about games on the site"
        )

    def test_get_statistics_on_the_site_success(self):
        response = self.client.get("/api/v1/game_info/statistic/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "Success")
        self.assertEqual(
            data["message"], "Successful get statistics about games on the site"
        )
        statistic = data["data"]
        self.assertEqual(statistic["played"], 0)
        self.assertEqual(statistic["number_of_teams"], 3)
        self.assertEqual(statistic["number_of_games"], 1)

    def test_get_statistics_on_the_site_no_sessions(self):
        # Видалення всіх ігрових сесій
        GameSession.objects.all().delete()

        response = self.client.get("/api/v1/game_info/statistic/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Success")
        self.assertIn("data", response.data)
        self.assertEqual(response.data["data"]["played"], 0)
        self.assertEqual(response.data["data"]["number_of_teams"], 0)
        self.assertEqual(response.data["data"]["number_of_games"], 1)

    def test_get_statistics_on_the_site_no_game_info(self):
        # Видалення всіх ігрових описів
        GameInfo.objects.all().delete()

        response = self.client.get("/api/v1/game_info/statistic/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Success")
        self.assertIn("data", response.data)
        self.assertEqual(response.data["data"]["played"], 0)
        self.assertEqual(response.data["data"]["number_of_games"], 0)
        self.assertEqual(response.data["data"]["number_of_teams"], 3)
