from django.http.cookie import SimpleCookie
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from players.dto import CreatePlayerDTO
from players.repositories import PlayerRepository


class PlayerTests(APITestCase):

    def setUp(self):

        self.url = reverse("api:players:players")
        repository = PlayerRepository()
        player = repository.create_player(
            CreatePlayerDTO(api_adress="api adress", browser_info="browser info")
        )
        self.player_uuid = player.player_uuid

    # --------------------------------------RETRIEVE PLAYER-----------------------------------------

    def test_player_retrieve_by_uuid_success(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": self.player_uuid})
        response = self.client.get(
            self.url, REMOTE_ADDR="api adress 2", HTTP_USER_AGENT="browser info 2"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful player retrieve")

        player = data["data"]
        self.assertEqual(player["api_adress"], "api adress")
        self.assertEqual(player["browser_info"], "browser info")
        self.assertEqual(player["username"], "Player")
        self.assertEqual(player["player_uuid"], self.player_uuid)

    def test_player_retrieve_by_options_success(self):

        response = self.client.get(
            self.url, REMOTE_ADDR="api adress", HTTP_USER_AGENT="browser info"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful player retrieve")

        player = data["data"]
        self.assertEqual(player["api_adress"], "api adress")
        self.assertEqual(player["browser_info"], "browser info")
        self.assertEqual(player["username"], "Player")
        self.assertEqual(player["player_uuid"], self.player_uuid)

    def test_player_retrieve_new_success(self):

        response = self.client.get(
            self.url, REMOTE_ADDR="api adress 2", HTTP_USER_AGENT="browser info 2"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful player retrieve")

        player = data["data"]
        self.assertEqual(player["api_adress"], "api adress 2")
        self.assertEqual(player["browser_info"], "browser info 2")
        self.assertEqual(player["username"], "Player")
        self.assertNotEqual(player["player_uuid"], self.player_uuid)

    # ---------------------------------------UPDATE PLAYER------------------------------------------
    def test_player_update_wrong_username_required(self):

        response = self.client.put(
            self.url,
            REMOTE_ADDR="api adress",
            HTTP_USER_AGENT="browser info",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.data
        self.assertEqual(data["status"], "failed")
        self.assertEqual(
            data["message"],
            "{'username': [ErrorDetail(string='This field is required.', code='required')]}",
        )

    def test_player_update_by_uuid_success(self):

        update_data = {
            "username": "Player 2",
        }
        self.client.cookies = SimpleCookie({"PLAYER_UUID": self.player_uuid})

        response = self.client.put(
            self.url, REMOTE_ADDR="api adress 2", HTTP_USER_AGENT="browser info 2", data=update_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful player update")

        player = data["data"]
        self.assertEqual(player["api_adress"], "api adress 2")
        self.assertEqual(player["browser_info"], "browser info 2")
        self.assertEqual(player["username"], "Player 2")
        self.assertEqual(player["player_uuid"], self.player_uuid)

    def test_player_update_by_options_success(self):

        update_data = {
            "username": "Player 2",
        }

        response = self.client.put(
            self.url, REMOTE_ADDR="api adress", HTTP_USER_AGENT="browser info", data=update_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful player update")

        player = data["data"]
        self.assertEqual(player["api_adress"], "api adress")
        self.assertEqual(player["browser_info"], "browser info")
        self.assertEqual(player["username"], "Player 2")
        self.assertEqual(player["player_uuid"], self.player_uuid)

    def test_player_update_new_success(self):

        update_data = {
            "username": "Player 3",
        }

        response = self.client.put(
            self.url, REMOTE_ADDR="api adress 3", HTTP_USER_AGENT="browser info 3", data=update_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful player update")

        player = data["data"]
        self.assertEqual(player["api_adress"], "api adress 3")
        self.assertEqual(player["browser_info"], "browser info 3")
        self.assertEqual(player["username"], "Player 3")
        self.assertNotEqual(player["player_uuid"], self.player_uuid)
