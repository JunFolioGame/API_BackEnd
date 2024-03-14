from django.http.cookie import SimpleCookie
from rest_framework import status
from rest_framework.test import APITestCase

from game_session.models import GameSession, identificator_generator
from game_session.repositories import GameSessionRepository
from players.models import Player
from players.repositories import PlayerRepository


class GameSessionTests(APITestCase):
    def setUp(self):
        self.url = "/api/v1/game_session/"

        player_repository = PlayerRepository()

        self.players = [
            player_repository.create_player().player_uuid for _ in range(24)
        ]

        self.game_session_repository = GameSessionRepository()

        self.game_session = GameSession.objects.create(
            creator=Player(player_uuid=self.players[0]),
            team_min=2,
            team_max=4,
            team_players_min=4,
            team_players_max=6,
        )

    # --------------------------------CREATE GAME SESSION-------------------------------
    def test_game_session_create_wrong_team_min_required(self):

        create_data = {
            "team_max": 1,
            "team_players_min": 1,
            "team_players_max": 1,
        }
        response = self.client.post(self.url, data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")

    def test_game_session_create_wrong_team_max_required(self):

        create_data = {
            "team_min": 1,
            "team_players_min": 1,
            "team_players_max": 1,
        }
        response = self.client.post(self.url, data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")

    def test_game_session_create_wrong_team_players_max_required(self):

        create_data = {
            "team_max": 1,
            "team_min": 1,
            "team_players_min": 1,
        }
        response = self.client.post(self.url, data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")

    def test_game_session_create_wrong_team_players_min_required(self):

        create_data = {
            "team_max": 1,
            "team_min": 1,
            "team_players_max": 1,
        }
        response = self.client.post(self.url, data=create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "failed")

    def test_game_session_create_success(self):

        create_data = {
            "team_min": 1,
            "team_max": 1,
            "team_players_min": 1,
            "team_players_max": 1,
        }
        response = self.client.post(self.url, data=create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful game session creation")
        game_session = data["data"]
        self.assertEqual(game_session["team_min"], 1)
        self.assertEqual(game_session["team_max"], 1)
        self.assertEqual(game_session["team_players_min"], 1)
        self.assertEqual(game_session["team_players_max"], 1)
        self.assertEqual(game_session["lobby"], [[]])

    # ---------------------------------FILL GAME SESSION--------------------------------
    def test_game_session_update_wrong_full(self):
        self.game_session.lobby.add(*self.players)
        response = self.client.put(
            self.url + f"{self.game_session.identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.data
        self.assertEqual(data["status"], "failed")
        self.assertEqual(
            data["message"],
            "['GameSession full of players']",
        )

    def test_game_session_update_wrong_not_found(self):
        while True:
            random_identificator = identificator_generator()
            if random_identificator != self.game_session.identificator:
                break

        response = self.client.put(
            self.url + f"{random_identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.data
        self.assertEqual(data["status"], "failed")
        self.assertEqual(
            data["message"],
            "GameSession doesn't exist",
        )

    def test_game_session_update_success(self):

        response = self.client.put(
            self.url + f"{self.game_session.identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Player successfully added in game session")

    # ---------------------------------GET SORTED TEAMS---------------------------------
    def test_game_session_teams_get_wrong_not_found(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": str(self.players[0])})
        while True:
            random_identificator = identificator_generator()
            if random_identificator != self.game_session.identificator:
                break

        response = self.client.get(
            self.url + f"{random_identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.data
        self.assertEqual(data["status"], "failed")
        self.assertEqual(
            data["message"],
            "GameSession doesn't exist",
        )

    def test_game_session_teams_get_wrong_not_enough_players(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": str(self.players[0])})
        response = self.client.get(
            self.url + f"{self.game_session.identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.data
        self.assertEqual(data["status"], "failed")
        self.assertEqual(
            data["message"],
            "['GameSession not enough players']",
        )

    def test_game_session_teams_get_success_eight_players(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": str(self.players[0])})
        self.game_session.lobby.add(*self.players[0:8])
        response = self.client.get(
            self.url + f"{self.game_session.identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful get game session")
        game_session = data["data"]
        self.assertEqual(game_session["team_min"], 2)
        self.assertEqual(game_session["team_max"], 4)
        self.assertEqual(game_session["team_players_min"], 4)
        self.assertEqual(game_session["team_players_max"], 6)
        teams = game_session["lobby"]
        self.assertEqual(len(teams), 2)
        self.assertEqual(len(teams[0]), 4)
        self.assertEqual(len(teams[1]), 4)

    def test_game_session_teams_get_success_nine_players(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": str(self.players[0])})
        self.game_session.lobby.add(*self.players[0:9])
        response = self.client.get(
            self.url + f"{self.game_session.identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful get game session")
        game_session = data["data"]
        self.assertEqual(game_session["team_min"], 2)
        self.assertEqual(game_session["team_max"], 4)
        self.assertEqual(game_session["team_players_min"], 4)
        self.assertEqual(game_session["team_players_max"], 6)
        teams = game_session["lobby"]
        self.assertEqual(len(teams), 2)
        self.assertEqual(len(teams[0]), 5)
        self.assertEqual(len(teams[1]), 4)

    def test_game_session_teams_get_success_ten_players(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": str(self.players[0])})
        self.game_session.lobby.add(*self.players[0:10])
        response = self.client.get(
            self.url + f"{self.game_session.identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful get game session")
        game_session = data["data"]
        self.assertEqual(game_session["team_min"], 2)
        self.assertEqual(game_session["team_max"], 4)
        self.assertEqual(game_session["team_players_min"], 4)
        self.assertEqual(game_session["team_players_max"], 6)
        teams = game_session["lobby"]
        self.assertEqual(len(teams), 2)
        self.assertEqual(len(teams[0]), 5)
        self.assertEqual(len(teams[1]), 5)

    def test_game_session_teams_get_success_eleven_players(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": str(self.players[0])})
        self.game_session.lobby.add(*self.players[0:11])
        response = self.client.get(
            self.url + f"{self.game_session.identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful get game session")
        game_session = data["data"]
        self.assertEqual(game_session["team_min"], 2)
        self.assertEqual(game_session["team_max"], 4)
        self.assertEqual(game_session["team_players_min"], 4)
        self.assertEqual(game_session["team_players_max"], 6)
        teams = game_session["lobby"]
        self.assertEqual(len(teams), 2)
        self.assertEqual(len(teams[0]), 6)
        self.assertEqual(len(teams[1]), 5)

    def test_game_session_teams_get_success_twelve_players(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": str(self.players[0])})
        self.game_session.lobby.add(*self.players[0:12])
        response = self.client.get(
            self.url + f"{self.game_session.identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful get game session")
        game_session = data["data"]
        self.assertEqual(game_session["team_min"], 2)
        self.assertEqual(game_session["team_max"], 4)
        self.assertEqual(game_session["team_players_min"], 4)
        self.assertEqual(game_session["team_players_max"], 6)
        teams = game_session["lobby"]
        self.assertEqual(len(teams), 3)
        self.assertEqual(len(teams[0]), 4)
        self.assertEqual(len(teams[1]), 4)
        self.assertEqual(len(teams[2]), 4)

    def test_game_session_teams_get_success_thirteen_players(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": str(self.players[0])})
        self.game_session.lobby.add(*self.players[0:13])
        response = self.client.get(
            self.url + f"{self.game_session.identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful get game session")
        game_session = data["data"]
        self.assertEqual(game_session["team_min"], 2)
        self.assertEqual(game_session["team_max"], 4)
        self.assertEqual(game_session["team_players_min"], 4)
        self.assertEqual(game_session["team_players_max"], 6)
        teams = game_session["lobby"]
        self.assertEqual(len(teams), 3)
        self.assertEqual(len(teams[0]), 5)
        self.assertEqual(len(teams[1]), 4)
        self.assertEqual(len(teams[2]), 4)

    def test_game_session_teams_get_success_fourteen_players(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": str(self.players[0])})
        self.game_session.lobby.add(*self.players[0:14])
        response = self.client.get(
            self.url + f"{self.game_session.identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful get game session")
        game_session = data["data"]
        self.assertEqual(game_session["team_min"], 2)
        self.assertEqual(game_session["team_max"], 4)
        self.assertEqual(game_session["team_players_min"], 4)
        self.assertEqual(game_session["team_players_max"], 6)
        teams = game_session["lobby"]
        self.assertEqual(len(teams), 3)
        self.assertEqual(len(teams[0]), 5)
        self.assertEqual(len(teams[1]), 5)
        self.assertEqual(len(teams[2]), 4)

    def test_game_session_teams_get_success_fifteen_players(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": str(self.players[0])})
        self.game_session.lobby.add(*self.players[0:15])
        response = self.client.get(
            self.url + f"{self.game_session.identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful get game session")
        game_session = data["data"]
        self.assertEqual(game_session["team_min"], 2)
        self.assertEqual(game_session["team_max"], 4)
        self.assertEqual(game_session["team_players_min"], 4)
        self.assertEqual(game_session["team_players_max"], 6)
        teams = game_session["lobby"]
        self.assertEqual(len(teams), 3)
        self.assertEqual(len(teams[0]), 5)
        self.assertEqual(len(teams[1]), 5)
        self.assertEqual(len(teams[2]), 5)

    def test_game_session_teams_get_success_sixteen_players(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": str(self.players[0])})
        self.game_session.lobby.add(*self.players[0:16])
        response = self.client.get(
            self.url + f"{self.game_session.identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful get game session")
        game_session = data["data"]
        self.assertEqual(game_session["team_min"], 2)
        self.assertEqual(game_session["team_max"], 4)
        self.assertEqual(game_session["team_players_min"], 4)
        self.assertEqual(game_session["team_players_max"], 6)
        teams = game_session["lobby"]
        self.assertEqual(len(teams), 4)
        self.assertEqual(len(teams[0]), 4)
        self.assertEqual(len(teams[1]), 4)
        self.assertEqual(len(teams[2]), 4)
        self.assertEqual(len(teams[3]), 4)

    def test_game_session_teams_get_success_seventeen_players(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": str(self.players[0])})
        self.game_session.lobby.add(*self.players[0:17])
        response = self.client.get(
            self.url + f"{self.game_session.identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful get game session")
        game_session = data["data"]
        self.assertEqual(game_session["team_min"], 2)
        self.assertEqual(game_session["team_max"], 4)
        self.assertEqual(game_session["team_players_min"], 4)
        self.assertEqual(game_session["team_players_max"], 6)
        teams = game_session["lobby"]
        self.assertEqual(len(teams), 4)
        self.assertEqual(len(teams[0]), 5)
        self.assertEqual(len(teams[1]), 4)
        self.assertEqual(len(teams[2]), 4)
        self.assertEqual(len(teams[3]), 4)

    def test_game_session_teams_get_success_eighteen_players(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": str(self.players[0])})
        self.game_session.lobby.add(*self.players[0:18])
        response = self.client.get(
            self.url + f"{self.game_session.identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful get game session")
        game_session = data["data"]
        self.assertEqual(game_session["team_min"], 2)
        self.assertEqual(game_session["team_max"], 4)
        self.assertEqual(game_session["team_players_min"], 4)
        self.assertEqual(game_session["team_players_max"], 6)
        teams = game_session["lobby"]
        self.assertEqual(len(teams), 3)
        self.assertEqual(len(teams[0]), 6)
        self.assertEqual(len(teams[1]), 6)
        self.assertEqual(len(teams[2]), 6)

    def test_game_session_teams_get_success_nineteen_players(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": str(self.players[0])})
        self.game_session.lobby.add(*self.players[0:19])
        response = self.client.get(
            self.url + f"{self.game_session.identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful get game session")
        game_session = data["data"]
        self.assertEqual(game_session["team_min"], 2)
        self.assertEqual(game_session["team_max"], 4)
        self.assertEqual(game_session["team_players_min"], 4)
        self.assertEqual(game_session["team_players_max"], 6)
        teams = game_session["lobby"]
        self.assertEqual(len(teams), 4)
        self.assertEqual(len(teams[0]), 5)
        self.assertEqual(len(teams[1]), 5)
        self.assertEqual(len(teams[2]), 5)
        self.assertEqual(len(teams[3]), 4)

    def test_game_session_teams_get_success_twenty_players(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": str(self.players[0])})
        self.game_session.lobby.add(*self.players[0:20])
        response = self.client.get(
            self.url + f"{self.game_session.identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful get game session")
        game_session = data["data"]
        self.assertEqual(game_session["team_min"], 2)
        self.assertEqual(game_session["team_max"], 4)
        self.assertEqual(game_session["team_players_min"], 4)
        self.assertEqual(game_session["team_players_max"], 6)
        teams = game_session["lobby"]
        self.assertEqual(len(teams), 4)
        self.assertEqual(len(teams[0]), 5)
        self.assertEqual(len(teams[1]), 5)
        self.assertEqual(len(teams[2]), 5)
        self.assertEqual(len(teams[3]), 5)

    def test_game_session_teams_get_success_twenty_one_players(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": str(self.players[0])})
        self.game_session.lobby.add(*self.players[0:21])
        response = self.client.get(
            self.url + f"{self.game_session.identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful get game session")
        game_session = data["data"]
        self.assertEqual(game_session["team_min"], 2)
        self.assertEqual(game_session["team_max"], 4)
        self.assertEqual(game_session["team_players_min"], 4)
        self.assertEqual(game_session["team_players_max"], 6)
        teams = game_session["lobby"]
        self.assertEqual(len(teams), 4)
        self.assertEqual(len(teams[0]), 6)
        self.assertEqual(len(teams[1]), 5)
        self.assertEqual(len(teams[2]), 5)
        self.assertEqual(len(teams[3]), 5)

    def test_game_session_teams_get_success_twenty_two_players(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": str(self.players[0])})
        self.game_session.lobby.add(*self.players[0:22])
        response = self.client.get(
            self.url + f"{self.game_session.identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful get game session")
        game_session = data["data"]
        self.assertEqual(game_session["team_min"], 2)
        self.assertEqual(game_session["team_max"], 4)
        self.assertEqual(game_session["team_players_min"], 4)
        self.assertEqual(game_session["team_players_max"], 6)
        teams = game_session["lobby"]
        self.assertEqual(len(teams), 4)
        self.assertEqual(len(teams[0]), 6)
        self.assertEqual(len(teams[1]), 6)
        self.assertEqual(len(teams[2]), 5)
        self.assertEqual(len(teams[3]), 5)

    def test_game_session_teams_get_success_twenty_three_players(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": str(self.players[0])})
        self.game_session.lobby.add(*self.players[0:23])
        response = self.client.get(
            self.url + f"{self.game_session.identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful get game session")
        game_session = data["data"]
        self.assertEqual(game_session["team_min"], 2)
        self.assertEqual(game_session["team_max"], 4)
        self.assertEqual(game_session["team_players_min"], 4)
        self.assertEqual(game_session["team_players_max"], 6)
        teams = game_session["lobby"]
        self.assertEqual(len(teams), 4)
        self.assertEqual(len(teams[0]), 6)
        self.assertEqual(len(teams[1]), 6)
        self.assertEqual(len(teams[2]), 6)
        self.assertEqual(len(teams[3]), 5)

    def test_game_session_teams_get_success_twenty_four_players(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": str(self.players[0])})
        self.game_session.lobby.add(*self.players[0:24])
        response = self.client.get(
            self.url + f"{self.game_session.identificator}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful get game session")
        game_session = data["data"]
        self.assertEqual(game_session["team_min"], 2)
        self.assertEqual(game_session["team_max"], 4)
        self.assertEqual(game_session["team_players_min"], 4)
        self.assertEqual(game_session["team_players_max"], 6)
        teams = game_session["lobby"]
        self.assertEqual(len(teams), 4)
        self.assertEqual(len(teams[0]), 6)
        self.assertEqual(len(teams[1]), 6)
        self.assertEqual(len(teams[2]), 6)
        self.assertEqual(len(teams[3]), 6)
