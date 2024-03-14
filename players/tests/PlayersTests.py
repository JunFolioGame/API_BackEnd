from uuid import uuid4

from django.http.cookie import SimpleCookie
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from players.repositories import PlayerRepository


class PlayerTests(APITestCase):

    def setUp(self):

        self.url = reverse("api:players:players")
        repository = PlayerRepository()
        player = repository.create_player()
        self.player_uuid = player.player_uuid

    # --------------------------------------RETRIEVE PLAYER-----------------------------

    def test_player_retrieve_wrong_bad_cookies(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": "111"})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.data
        self.assertEqual(data["status"], "failed")
        self.assertEqual(data["message"], "['111 is not a valid UUID']")

    def test_player_retrieve_wrong_player_dont_exist(self):
        while True:
            random_uuid = uuid4()
            if random_uuid != self.player_uuid:
                break
        self.client.cookies = SimpleCookie({"PLAYER_UUID": str(random_uuid)})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        data = response.data
        self.assertEqual(data["status"], "failed")
        self.assertEqual(data["message"], "Player doesn't exist")

    def test_player_retrieve_by_uuid_success(self):
        self.client.cookies = SimpleCookie({"PLAYER_UUID": self.player_uuid})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful player retrieve")

        player = data["data"]
        self.assertEqual(player["username"], "Player")
        self.assertEqual(player["player_uuid"], self.player_uuid)

    def test_player_retrieve_new_success(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful player retrieve")

        player = data["data"]
        self.assertEqual(player["username"], "Player")
        self.assertNotEqual(player["player_uuid"], self.player_uuid)

    # ---------------------------------------UPDATE PLAYER------------------------------
    def test_player_update_wrong_player_dont_exist(self):

        while True:
            random_uuid = uuid4()
            if random_uuid != self.player_uuid:
                break

        update_data = {
            "username": "Player 2",
        }
        self.client.cookies = SimpleCookie({"PLAYER_UUID": str(random_uuid)})
        response = self.client.put(
            self.url,
            data=update_data,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        data = response.data
        self.assertEqual(data["status"], "failed")
        self.assertEqual(data["message"], "Player doesn't exist")

    def test_player_update_wrong_username_required(self):

        response = self.client.put(
            self.url,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.data
        self.assertEqual(data["status"], "failed")

    def test_player_update_by_uuid_success(self):

        update_data = {
            "username": "Player 2",
        }
        self.client.cookies = SimpleCookie({"PLAYER_UUID": self.player_uuid})

        response = self.client.put(
            self.url,
            data=update_data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful player update")

        player = data["data"]
        self.assertEqual(player["username"], "Player 2")
        self.assertEqual(player["player_uuid"], self.player_uuid)

    def test_player_update_new_success(self):

        update_data = {
            "username": "Player 3",
        }

        response = self.client.put(
            self.url,
            data=update_data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful player update")

        player = data["data"]
        self.assertEqual(player["username"], "Player 3")
        self.assertNotEqual(player["player_uuid"], self.player_uuid)
