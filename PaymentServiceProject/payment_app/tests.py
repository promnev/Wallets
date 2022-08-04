from django.contrib.auth.models import User
from payment_app.Transactions.models import Transaction
from payment_app.Wallets.models import Wallet
from rest_framework import status
from rest_framework.test import APITestCase


class AppTests(APITestCase):
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
        data1 = {"username": "loslos321", "password": "pospospos123"}
        test_user = User.objects.create_user(
            "loslos321", password="pospospos123"
        )
        test_user.save()
        response = self.client.post("auth/token/login/", data1, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        data1 = {"username": "loslos", "password": "pospospos"}
        test_user = User.objects.create_user("loslos", password="pospospos")
        test_user.save()
        response = self.client.post("auth/token/login/", data1, format="json")
        token_from_response = response.data["auth_token"]
        token = "Token " + str(token_from_response)
        response = self.client.post(
            "auth/token/logout/", HTTP_AUTHORIZATION=token, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_wallet_create(self):
        data1 = {"username": "loslos", "password": "pospospos"}
        test_user = User.objects.create_user("loslos", password="pospospos")
        test_user.save()
        response = self.client.post("/auth/token/login/", data1, format="json")
        token_from_response = response.data["auth_token"]
        token = "Token " + str(token_from_response)
        data = {"type": "Visa", "currency": "USD"}
        response = self.client.post(
            "/api/v1/wallets/", data, HTTP_AUTHORIZATION=token, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Wallet.objects.count(), 1)
        self.assertEqual(Wallet.objects.get().type, "Visa")
        self.assertEqual(Wallet.objects.get().currency, "USD")

    def test_get_all_wallets_for_current_user(self):
        data1 = {"username": "loslos", "password": "pospospos"}
        test_user = User.objects.create_user("loslos", password="pospospos")
        test_user.save()
        response = self.client.post("/auth/token/login/", data1, format="json")
        token_from_response = response.data["auth_token"]
        token = "Token " + str(token_from_response)
        data = {"type": "Visa", "currency": "USD"}
        self.client.post(
            "/api/v1/wallets/", data, HTTP_AUTHORIZATION=token, format="json"
        )
        self.client.post(
            "/api/v1/wallets/", data, HTTP_AUTHORIZATION=token, format="json"
        )
        response = self.client.get(
            "/api/v1/wallets/", HTTP_AUTHORIZATION=token, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual((response.data[0])["id"], 1)
        self.assertEqual((response.data[1])["id"], 2)
        self.assertEqual(
            Wallet.objects.get(pk=1).user.username,
            User.objects.first().username,
        )
        self.assertEqual(
            Wallet.objects.get(pk=2).user.username,
            User.objects.first().username,
        )

    def test_get_wallet_by_name(self):
        data1 = {"username": "loslos", "password": "pospospos"}
        test_user = User.objects.create_user("loslos", password="pospospos")
        test_user.save()
        response = self.client.post("/auth/token/login/", data1, format="json")
        token_from_response = response.data["auth_token"]
        token = "Token " + str(token_from_response)
        data = {"type": "Visa", "currency": "USD"}
        self.client.post(
            "/api/v1/wallets/", data, HTTP_AUTHORIZATION=token, format="json"
        )
        wallet_name = Wallet.objects.first()
        response = self.client.get(
            f"/api/v1/wallets/{wallet_name}/",
            HTTP_AUTHORIZATION=token,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], wallet_name.name)

    def test_wallet_delete(self):
        data1 = {"username": "loslos", "password": "pospospos"}
        test_user = User.objects.create_user("loslos", password="pospospos")
        test_user.save()
        response = self.client.post("/auth/token/login/", data1, format="json")
        token_from_response = response.data["auth_token"]
        token = "Token " + str(token_from_response)
        data = {"type": "Visa", "currency": "USD"}
        self.client.post(
            "/api/v1/wallets/", data, HTTP_AUTHORIZATION=token, format="json"
        )
        wallet_name = Wallet.objects.first()
        response = self.client.delete(
            f"/api/v1/wallets/{wallet_name}/",
            HTTP_AUTHORIZATION=token,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Wallet.objects.count(), 0)

    def test_transaction_create(self):
        data1 = {"username": "loslos", "password": "pospospos"}
        test_user = User.objects.create_user("loslos", password="pospospos")
        test_user.save()
        response = self.client.post("/auth/token/login/", data1, format="json")
        token_from_response = response.data["auth_token"]
        token = "Token " + str(token_from_response)
        data = {"type": "Visa", "currency": "USD"}
        self.client.post(
            "/api/v1/wallets/", data, HTTP_AUTHORIZATION=token, format="json"
        )
        receiver_wallet_name = Wallet.objects.get(pk=1).name
        self.client.post(
            "/auth/token/logout/", HTTP_AUTHORIZATION=token, format="json"
        )

        data1 = {
            "username": "testwereruser2423432",
            "password": "fdsfsfpassfsdfdsf3242",
        }
        test_user2 = User.objects.create_user(
            "testwereruser2423432", password="fdsfsfpassfsdfdsf3242"
        )
        test_user2.save()
        response = self.client.post("/auth/token/login/", data1, format="json")
        token_from_response = response.data["auth_token"]
        token = "Token " + str(token_from_response)
        data = {"type": "Visa", "currency": "USD"}
        self.client.post(
            "/api/v1/wallets/", data, HTTP_AUTHORIZATION=token, format="json"
        )
        sender_wallet_name = Wallet.objects.get(pk=2).name

        data2 = {
            "sender": sender_wallet_name,
            "receiver": receiver_wallet_name,
            "transfer_amount": 1,
        }
        response = self.client.post(
            "/api/v1/transactions/",
            data2,
            HTTP_AUTHORIZATION=token,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Transaction.objects.first().sender.name, sender_wallet_name
        )
        self.assertEqual(
            Transaction.objects.first().receiver.name, receiver_wallet_name
        )

    def test_get_all_transactions_for_current_user(self):
        data1 = {"username": "loslos", "password": "pospospos"}
        test_user = User.objects.create_user("loslos", password="pospospos")
        test_user.save()
        response = self.client.post("/auth/token/login/", data1, format="json")
        token_from_response = response.data["auth_token"]
        token = "Token " + str(token_from_response)
        data = {"type": "Visa", "currency": "USD"}
        self.client.post(
            "/api/v1/wallets/", data, HTTP_AUTHORIZATION=token, format="json"
        )
        receiver_wallet_name = Wallet.objects.get(pk=1).name
        self.client.post(
            "/auth/token/logout/", HTTP_AUTHORIZATION=token, format="json"
        )

        data1 = {
            "username": "testwereruser2423432",
            "password": "fdsfsfpassfsdfdsf3242",
        }
        test_user2 = User.objects.create_user(
            "testwereruser2423432", password="fdsfsfpassfsdfdsf3242"
        )
        test_user2.save()
        response = self.client.post("/auth/token/login/", data1, format="json")
        token_from_response = response.data["auth_token"]
        token = "Token " + str(token_from_response)
        data = {"type": "Visa", "currency": "USD"}
        self.client.post(
            "/api/v1/wallets/", data, HTTP_AUTHORIZATION=token, format="json"
        )
        sender_wallet_name = Wallet.objects.get(pk=2).name

        data2 = {
            "sender": sender_wallet_name,
            "receiver": receiver_wallet_name,
            "transfer_amount": 1,
        }
        self.client.post(
            "/api/v1/transactions/",
            data2,
            HTTP_AUTHORIZATION=token,
            format="json",
        )
        self.client.post(
            "/api/v1/transactions/",
            data2,
            HTTP_AUTHORIZATION=token,
            format="json",
        )

        response = self.client.get(
            "/api/v1/transactions/", HTTP_AUTHORIZATION=token, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual((response.data[0])["id"], 1)
        self.assertEqual((response.data[1])["id"], 2)
        self.assertEqual((response.data[0])["sender"], sender_wallet_name)
        self.assertEqual((response.data[1])["sender"], sender_wallet_name)
        self.assertEqual((response.data[0])["receiver"], receiver_wallet_name)
        self.assertEqual((response.data[1])["receiver"], receiver_wallet_name)

    def test_get_transaction_by_id(self):
        data1 = {"username": "loslos", "password": "pospospos"}
        test_user = User.objects.create_user("loslos", password="pospospos")
        test_user.save()
        response = self.client.post("/auth/token/login/", data1, format="json")
        token_from_response = response.data["auth_token"]
        token = "Token " + str(token_from_response)
        data = {"type": "Visa", "currency": "USD"}
        self.client.post(
            "/api/v1/wallets/", data, HTTP_AUTHORIZATION=token, format="json"
        )
        receiver_wallet_name = Wallet.objects.get(pk=1).name
        self.client.post(
            "/auth/token/logout/", HTTP_AUTHORIZATION=token, format="json"
        )

        data1 = {
            "username": "testwereruser2423432",
            "password": "fdsfsfpassfsdfdsf3242",
        }
        test_user2 = User.objects.create_user(
            "testwereruser2423432", password="fdsfsfpassfsdfdsf3242"
        )
        test_user2.save()
        response = self.client.post("/auth/token/login/", data1, format="json")
        token_from_response = response.data["auth_token"]
        token = "Token " + str(token_from_response)
        data = {"type": "Visa", "currency": "USD"}
        self.client.post(
            "/api/v1/wallets/", data, HTTP_AUTHORIZATION=token, format="json"
        )
        sender_wallet_name = Wallet.objects.get(pk=2).name

        data2 = {
            "sender": sender_wallet_name,
            "receiver": receiver_wallet_name,
            "transfer_amount": 1,
        }
        self.client.post(
            "/api/v1/transactions/",
            data2,
            HTTP_AUTHORIZATION=token,
            format="json",
        )

        response = self.client.get(
            "/api/v1/transactions/1/",
            data2,
            HTTP_AUTHORIZATION=token,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 1)

    def test_get_all_transactions_by_wallet_name_where_it_is_sender_or_receiver(
        self,
    ):

        data1 = {"username": "loslos", "password": "pospospos"}
        test_user = User.objects.create_user("loslos", password="pospospos")
        test_user.save()
        response = self.client.post("/auth/token/login/", data1, format="json")
        token_from_response = response.data["auth_token"]
        token = "Token " + str(token_from_response)
        data = {"type": "Visa", "currency": "USD"}
        self.client.post(
            "/api/v1/wallets/", data, HTTP_AUTHORIZATION=token, format="json"
        )
        receiver_wallet_name = Wallet.objects.get(pk=1).name
        self.client.post(
            "/auth/token/logout/", HTTP_AUTHORIZATION=token, format="json"
        )

        data1 = {
            "username": "fsdfsdfsdf2423432",
            "password": "fdsfsfdsfdsfdsfdsfsdfsjghgdsf3242",
        }
        test_user2 = User.objects.create_user(
            "fsdfsdfsdf2423432", password="fdsfsfdsfdsfdsfdsfsdfsjghgdsf3242"
        )
        test_user2.save()
        response = self.client.post("/auth/token/login/", data1, format="json")
        token_from_response = response.data["auth_token"]
        token = "Token " + str(token_from_response)
        data = {"type": "Visa", "currency": "USD"}
        self.client.post(
            "/api/v1/wallets/", data, HTTP_AUTHORIZATION=token, format="json"
        )
        third_user_wallet_name = Wallet.objects.get(pk=2).name

        # create transaction from third_user to receiver, which shouldn't be returned in final responce ( transaction id = 1 )
        data2 = {
            "sender": third_user_wallet_name,
            "receiver": receiver_wallet_name,
            "transfer_amount": 1,
        }
        self.client.post(
            "/api/v1/transactions/",
            data2,
            HTTP_AUTHORIZATION=token,
            format="json",
        )

        data1 = {
            "username": "testwereruser2423432",
            "password": "fdsfsfpassfsdfdsf3242",
        }
        test_user2 = User.objects.create_user(
            "testwereruser2423432", password="fdsfsfpassfsdfdsf3242"
        )
        test_user2.save()
        response = self.client.post("/auth/token/login/", data1, format="json")
        token_from_response = response.data["auth_token"]
        token = "Token " + str(token_from_response)
        data = {"type": "Visa", "currency": "USD"}
        self.client.post(
            "/api/v1/wallets/", data, HTTP_AUTHORIZATION=token, format="json"
        )
        sender_wallet_name = Wallet.objects.get(pk=3).name

        data2 = {
            "sender": sender_wallet_name,
            "receiver": receiver_wallet_name,
            "transfer_amount": 1,
        }
        self.client.post(
            "/api/v1/transactions/",
            data2,
            HTTP_AUTHORIZATION=token,
            format="json",
        )
        self.client.post(
            "/api/v1/transactions/",
            data2,
            HTTP_AUTHORIZATION=token,
            format="json",
        )

        response = self.client.get(
            f"/api/v1/transactions/wallet/{sender_wallet_name}/",
            HTTP_AUTHORIZATION=token,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual((response.data[0])["id"], 2)
        self.assertEqual((response.data[1])["id"], 3)
