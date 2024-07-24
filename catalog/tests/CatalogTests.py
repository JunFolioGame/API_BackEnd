import os

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from additional_service.upload_delete_file import AdditionalService
from catalog.dto import CreateGameInfoDTO
from catalog.models import GameInfo
from catalog.repositories import GameInfoRepository
from game_session.models import GameSession
from game_session.repositories import GameSessionRepository
from players.models import Player
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

        game1 = repository.create_game_info(
            CreateGameInfoDTO(
                name_ua="Game1 Name UA",
                name_en="Game1 Name EN",
                photo="test.jpg",
                description_ua="Game1 Description UA",
                description_en="Game1 Description EN",
                is_team=True,
                members=1,
            )
        )
        self.game1_uuid = game1.uuid

        game2 = repository.create_game_info(
            CreateGameInfoDTO(
                name_ua="Game2 Name UA",
                name_en="Game2 Name EN",
                photo="test.jpg",
                description_ua="Game 2 Description UA",
                description_en="Game 2 Description EN",
                is_team=False,
                members=1,
            )
        )
        self.game2_uuid = game2.uuid

        game3 = repository.create_game_info(
            CreateGameInfoDTO(
                name_ua="Game3 Name UA",
                name_en="Game3 Name EN",
                photo="test.jpg",
                description_ua="Game3 Description UA",
                description_en="Game3 Description EN",
                is_team=True,
                members=5,
            )
        )
        self.game3_uuid = game3.uuid

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

        game = response.data["data"]
        self.assertEqual(game["name_ua"], "Test Name UA 2")
        self.assertEqual(game["name_en"], "Test Name EN 2")
        self.assertEqual(game["description_ua"], "Test Description UA 2")
        self.assertEqual(game["description_en"], "Test Description EN 2")
        self.assertEqual(game["members"], 10)
        # Видаляємо фото, щоб не засмічувати пам'ять
        AdditionalService.delete_file_from_s3(self, photo_url=game["photo"])

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

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")

    # Positive test case for ApiGameInfoView get method
    def test_get_game_info_success(self):
        uuid = self.game_info_uuid
        response = self.client.get(f"/api/v1/game_info/{uuid}/")
        assert response.status_code == 200
        assert response.data["status"] == "success"
        assert response.data["message"] == "Successful get game_info information"

        game = response.data["data"]
        self.assertEqual(game["name_ua"], "Test Name UA")
        self.assertEqual(game["name_en"], "Test Name EN")
        self.assertEqual(game["description_ua"], "Test Description UA")
        self.assertEqual(game["description_en"], "Test Description EN")
        self.assertEqual(game["photo"], "test.jpg")
        self.assertEqual(game["is_team"], False)
        self.assertEqual(game["members"], 10)

    # Negative test case for ApiGameInfoView get method
    def test_get_game_info_failure_not_found(self):
        uuid = "invalid-uuid"
        response = self.client.get(f"/api/v1/game_info/{uuid}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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

        game = response.data["data"]
        self.assertEqual(game["name_ua"], "Updated Name UA")
        self.assertEqual(game["name_en"], "Updated Name EN")
        self.assertEqual(game["description_ua"], "Updated Description UA")
        self.assertEqual(game["description_en"], "Updated Description EN")
        self.assertEqual(game["is_team"], True)
        self.assertEqual(game["is_active"], False)
        self.assertEqual(game["members"], 20)
        # Видаляємо фото, щоб не засмічувати пам'ять
        AdditionalService.delete_file_from_s3(self, photo_url=game["photo"])

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

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Positive test case for APIAllGameInfoView get method
    def test_get_all_game_info_success(self):
        response = self.client.get("/api/v1/game_info/all/")
        assert response.status_code == 200
        assert response.data["status"] == "Success"
        assert response.data["message"] == "Successful get list of all game_info"

        game = response.data["data"][0]
        self.assertEqual(game["name_ua"], "Test Name UA")
        self.assertEqual(game["name_en"], "Test Name EN")
        self.assertEqual(game["description_ua"], "Test Description UA")
        self.assertEqual(game["description_ua"], "Test Description UA")
        self.assertEqual(game["description_en"], "Test Description EN")
        self.assertEqual(game["is_team"], False)
        self.assertEqual(game["is_active"], False)
        self.assertEqual(game["members"], 10)

    def test_get_statistics_on_the_site(self):
        response = self.client.get("/api/v1/game_info/statistic/")
        assert response.status_code == 200
        assert response.data["status"] == "Success"
        assert (
            response.data["message"]
            == "Successful get statistics about games on the site"
        )

        game = response.data["data"]
        self.assertEqual(game["played"], 0)
        self.assertEqual(game["number_of_teams"], 3)
        self.assertEqual(game["number_of_games"], 4)

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
        self.assertEqual(statistic["number_of_games"], 4)

    def test_get_statistics_on_the_site_no_sessions(self):
        # Видалення всіх ігрових сесій
        GameSession.objects.all().delete()

        response = self.client.get("/api/v1/game_info/statistic/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Success")
        self.assertIn("data", response.data)
        self.assertEqual(response.data["data"]["played"], 0)
        self.assertEqual(response.data["data"]["number_of_teams"], 0)
        self.assertEqual(response.data["data"]["number_of_games"], 4)

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

    def test_create_category_wrong_empty(self):
        create_data = {}
        response = self.client.post("/api/v1/game_info/", data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")

    def test_category_create_wrong_name_ua_required(self):
        create_data = {
            "name_en": "test_2",
            "description_ua": "test_2",
            "description_en": "test_2",
            "is_active": True,
        }

        response = self.client.post("/api/v1/game_info/", data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")

    def test_create_category_wrong_name_en_required(self):
        create_data = {
            "name_ua": "test_2",
            "description_ua": "test_2",
            "description_en": "test_2",
            "is_active": True,
        }
        response = self.client.post("/api/v1/game_info/", data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")

    def test_create_category_wrong_description_ua_required(self):
        create_data = {
            "name_ua": "test_2",
            "name_en": "test_2",
            "description_en": "test_2",
            "is_active": True,
        }
        response = self.client.post("/api/v1/game_info/", data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")

    def test_create_category_wrong_description_en_required(self):
        create_data = {
            "name_ua": "test_2",
            "name_en": "test_2",
            "description_ua": "test_2",
            "is_active": True,
        }
        response = self.client.post("/api/v1/game_info/", data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")

    def test_create_category_wrong_bad_photo(self):
        create_data = {
            "name_ua": "test_2",
            "name_en": "test_2",
            "description_ua": "test_2",
            "description_en": "test_2",
            "is_active": True,
            "photo_jpeg": self.wrong_photo_jpeg,
        }
        response = self.client.post("/api/v1/game_info/", data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")

    def test_group_games_filter(self):
        group_data = {"group_or_individual": "group"}
        response = self.client.post("/api/v1/game_info/all/", data=group_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Success")
        self.assertEqual(
            response.data["message"],
            "Successfully received an all game info, "
            "                or with additional filtering and sorted",
        )
        self.assertEqual(len(response.data["data"]), 2)

    def test_individual_games_filter(self):
        individual_data = {"group_or_individual": "individual"}
        response = self.client.post("/api/v1/game_info/all/", data=individual_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Success")
        self.assertEqual(
            response.data["message"],
            "Successfully received an all game info, "
            "                or with additional filtering and sorted",
        )
        self.assertEqual(response.data["data"][0]["members"], 1)
        self.assertEqual(len(response.data["data"]), 2)

    def test_sort_by_popularity(self):
        popularity_data = {"sort_selection": "popularity"}
        response = self.client.post("/api/v1/game_info/all/", data=popularity_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Success")
        self.assertEqual(
            response.data["message"],
            "Successfully received an all game info,\
                 or with additional filtering and sorted",
        )
        self.assertEqual(response.data["data"][0]["name_ua"], "Test Name UA")
        self.assertEqual(response.data["data"][1]["name_ua"], "Game1 Name UA")
        self.assertEqual(response.data["data"][2]["name_ua"], "Game2 Name UA")
        self.assertEqual(response.data["data"][3]["name_ua"], "Game3 Name UA")

    def test_sort_by_newness(self):
        newness_data = {"sort_selection": "newness"}
        response = self.client.post("/api/v1/game_info/all/", data=newness_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Success")
        self.assertEqual(
            response.data["message"],
            "Successfully received an all game info,\
                 or with additional filtering and sorted",
        )
        self.assertEqual(response.data["data"][0]["name_ua"], "Game3 Name UA")
        self.assertEqual(response.data["data"][1]["name_ua"], "Game2 Name UA")
        self.assertEqual(response.data["data"][2]["name_ua"], "Game1 Name UA")

    def test_sort_by_members(self):
        members_data = {"sort_selection": "member"}
        response = self.client.post("/api/v1/game_info/all/", data=members_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Success")
        self.assertEqual(
            response.data["message"],
            "Successfully received an all game info,\
                 or with additional filtering and sorted",
        )
        self.assertEqual(response.data["data"][0]["name_ua"], "Test Name UA")
        self.assertEqual(response.data["data"][1]["name_ua"], "Game3 Name UA")
        self.assertEqual(response.data["data"][2]["name_ua"], "Game1 Name UA")
        self.assertEqual(response.data["data"][3]["name_ua"], "Game2 Name UA")
