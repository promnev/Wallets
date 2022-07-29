from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class AccountTests(APITestCase):
    def test_create_account(self):
        data = {
            "username": "testunsdfsddfsfssfiquename",
            "password": "887sfsuep2342424ass",
        }
        response = self.client.post("/api/v1/auth/users/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(
            User.objects.get().username, "testunsdfsddfsfssfiquename"
        )

    def test_login(self):
        data1 = {"username": "loslos", "password": "pospospos"}
        test_user = User.objects.create_user("loslos", password="pospospos")
        test_user.save()
        response = self.client.post("/auth/token/login/", data1, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        data1 = {"username": "loslos", "password": "pospospos"}
        test_user = User.objects.create_user("loslos", password="pospospos")
        test_user.save()
        response = self.client.post("/auth/token/login/", data1, format="json")
        token_from_response = response.data["auth_token"]
        token = "Token " + str(token_from_response)
        response = self.client.post(
            "/auth/token/logout/", HTTP_AUTHORIZATION=token, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
