import pytest
from payment_app.Transactions.models import Transaction
from payment_app.Wallets.models import Wallet
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_transaction_create():
    payload = {
        "username": "harrypotter1988",
        "password": "hogwarts2000",
    }
    client.post("/api/v1/registration/users/", payload)
    response = client.post("/auth/token/login/", payload)
    token_from_response = response.data["auth_token"]
    token = "Token " + str(token_from_response)
    data = {"type": "Visa", "currency": "USD"}
    client.post("/api/v1/wallets/", data, HTTP_AUTHORIZATION=token)
    receiver_wallet_name = Wallet.objects.first().name
    client.post("/auth/token/logout/", HTTP_AUTHORIZATION=token)

    payload2 = {
        "username": "germionagranger1990",
        "password": "fsdf32424sfsf",
    }
    client.post("/api/v1/registration/users/", payload2)
    response = client.post("/auth/token/login/", payload2)
    token_from_response = response.data["auth_token"]
    token = "Token " + str(token_from_response)
    data = {"type": "Mastercard", "currency": "USD"}
    response = client.post("/api/v1/wallets/", data, HTTP_AUTHORIZATION=token)
    #
    sender_wallet_name = Wallet.objects.get(type="Mastercard").name

    transaction_data = {
        "sender": sender_wallet_name,
        "receiver": receiver_wallet_name,
        "transfer_amount": 1,
    }
    response = client.post(
        "/api/v1/transactions/", transaction_data, HTTP_AUTHORIZATION=token
    )
    assert response.status_code == 200
    assert Transaction.objects.first().sender.name == sender_wallet_name
    assert Transaction.objects.first().receiver.name == receiver_wallet_name


@pytest.mark.django_db
def test_get_all_transactions_for_current_user():
    payload = {
        "username": "harrypotter1988",
        "password": "hogwarts2000",
    }
    client.post("/api/v1/registration/users/", payload)
    response = client.post("/auth/token/login/", payload)
    token_from_response = response.data["auth_token"]
    token = "Token " + str(token_from_response)
    data = {"type": "Visa", "currency": "USD"}
    client.post("/api/v1/wallets/", data, HTTP_AUTHORIZATION=token)
    receiver_wallet_name = Wallet.objects.first().name
    client.post("/auth/token/logout/", HTTP_AUTHORIZATION=token)

    payload2 = {
        "username": "germionagranger1990",
        "password": "fsdf32424sfsf",
    }
    client.post("/api/v1/registration/users/", payload2)
    response = client.post("/auth/token/login/", payload2)
    token_from_response = response.data["auth_token"]
    token = "Token " + str(token_from_response)
    data = {"type": "Mastercard", "currency": "USD"}
    client.post("/api/v1/wallets/", data, HTTP_AUTHORIZATION=token)
    sender_wallet_name = Wallet.objects.get(type="Mastercard").name

    transaction_data = {
        "sender": sender_wallet_name,
        "receiver": receiver_wallet_name,
        "transfer_amount": 1,
    }
    client.post(
        "/api/v1/transactions/", transaction_data, HTTP_AUTHORIZATION=token
    )
    client.post(
        "/api/v1/transactions/", transaction_data, HTTP_AUTHORIZATION=token
    )
    response = client.get("/api/v1/transactions/", HTTP_AUTHORIZATION=token)
    assert response.status_code == 200
    assert (response.data[0])["sender"] == sender_wallet_name
    assert (response.data[1])["sender"] == sender_wallet_name
    assert (response.data[0])["receiver"] == receiver_wallet_name
    assert (response.data[1])["receiver"] == receiver_wallet_name


@pytest.mark.django_db
def test_get_transaction_by_id():
    payload = {
        "username": "harrypotter1988",
        "password": "hogwarts2000",
    }
    client.post("/api/v1/registration/users/", payload)
    response = client.post("/auth/token/login/", payload)
    token_from_response = response.data["auth_token"]
    token = "Token " + str(token_from_response)
    data = {"type": "Visa", "currency": "USD"}
    client.post("/api/v1/wallets/", data, HTTP_AUTHORIZATION=token)
    receiver_wallet_name = Wallet.objects.first().name
    client.post("/auth/token/logout/", HTTP_AUTHORIZATION=token)

    payload2 = {
        "username": "germionagranger1990",
        "password": "fsdf32424sfsf",
    }
    client.post("/api/v1/registration/users/", payload2)
    response = client.post("/auth/token/login/", payload2)
    token_from_response = response.data["auth_token"]
    token = "Token " + str(token_from_response)
    data = {"type": "Mastercard", "currency": "USD"}
    client.post("/api/v1/wallets/", data, HTTP_AUTHORIZATION=token)
    sender_wallet_name = Wallet.objects.get(type="Mastercard").name

    transaction_data = {
        "sender": sender_wallet_name,
        "receiver": receiver_wallet_name,
        "transfer_amount": 1,
    }
    response = client.post(
        "/api/v1/transactions/", transaction_data, HTTP_AUTHORIZATION=token
    )
    transaction_id = response.data["id"]

    response = client.get(
        f"/api/v1/transactions/{transaction_id}/", HTTP_AUTHORIZATION=token
    )
    assert response.status_code == 200
    assert response.data["id"] == transaction_id


@pytest.mark.django_db
def test_get_all_transactions_by_wallet_name_where_it_is_sender_or_receiver():
    payload = {
        "username": "harrypotter1988",
        "password": "hogwarts2000",
    }
    client.post("/api/v1/registration/users/", payload)
    response = client.post("/auth/token/login/", payload)
    token_from_response = response.data["auth_token"]
    token = "Token " + str(token_from_response)
    data = {"type": "Visa", "currency": "USD"}
    client.post("/api/v1/wallets/", data, HTTP_AUTHORIZATION=token)
    receiver_wallet_name = Wallet.objects.first().name
    client.post("/auth/token/logout/", HTTP_AUTHORIZATION=token)

    payload3 = {
        "username": "ronwisley",
        "password": "redhairscool",
    }
    client.post("/api/v1/registration/users/", payload3)
    response = client.post("/auth/token/login/", payload3)
    token_from_response = response.data["auth_token"]
    token = "Token " + str(token_from_response)
    data = {"type": "Visa", "currency": "USD"}
    response = client.post("/api/v1/wallets/", data, HTTP_AUTHORIZATION=token)
    third_user_wallet_id = response.data["id"]
    third_user_wallet_name = Wallet.objects.get(id=third_user_wallet_id).name
    client.post("/auth/token/logout/", HTTP_AUTHORIZATION=token)

    # create transaction from third_user to receiver, which shouldn't be returned in final responce ( transaction id = 1 )
    data2 = {
        "sender": third_user_wallet_name,
        "receiver": receiver_wallet_name,
        "transfer_amount": 1,
    }
    client.post("/api/v1/transactions/", data2, HTTP_AUTHORIZATION=token)

    payload2 = {
        "username": "germionagranger1990",
        "password": "fsdf32424sfsf",
    }
    client.post("/api/v1/registration/users/", payload2)
    response = client.post("/auth/token/login/", payload2)
    token_from_response = response.data["auth_token"]
    token = "Token " + str(token_from_response)
    data = {"type": "Mastercard", "currency": "USD"}
    client.post("/api/v1/wallets/", data, HTTP_AUTHORIZATION=token)
    sender_wallet_name = Wallet.objects.get(type="Mastercard").name

    transaction_data = {
        "sender": sender_wallet_name,
        "receiver": receiver_wallet_name,
        "transfer_amount": 1,
    }
    client.post(
        "/api/v1/transactions/", transaction_data, HTTP_AUTHORIZATION=token
    )
    client.post(
        "/api/v1/transactions/", transaction_data, HTTP_AUTHORIZATION=token
    )
    response = client.get("/api/v1/transactions/", HTTP_AUTHORIZATION=token)
    assert response.status_code == 200
    assert (response.data[0])["sender"] == sender_wallet_name
    assert (response.data[1])["sender"] == sender_wallet_name
    assert (response.data[0])["receiver"] == receiver_wallet_name
    assert (response.data[1])["receiver"] == receiver_wallet_name
    assert third_user_wallet_name not in response.data
