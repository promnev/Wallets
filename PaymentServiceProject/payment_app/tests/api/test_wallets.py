import pytest
from payment_app.Wallets.models import Wallet
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_wallet_create():
    payload = {
        "username": "harrypotter1988",
        "password": "hogwarts2000",
    }
    client.post("/api/v1/registration/users/", payload)
    response = client.post("/auth/token/login/", payload)
    token_from_response = response.data["auth_token"]
    token = "Token " + str(token_from_response)
    data = {"type": "Visa", "currency": "USD"}
    response = client.post("/api/v1/wallets/", data, HTTP_AUTHORIZATION=token)
    assert response.status_code == 200
    assert Wallet.objects.count() == 1
    assert Wallet.objects.get().type == "Visa"
    assert Wallet.objects.get().currency == "USD"


@pytest.mark.django_db
def test_get_all_wallets_for_current_user():
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
    client.post("/api/v1/wallets/", data, HTTP_AUTHORIZATION=token)
    response = client.get("/api/v1/wallets/", HTTP_AUTHORIZATION=token)
    assert response.status_code == 200
    assert Wallet.objects.count() == len(response.data)


@pytest.mark.django_db
def test_get_wallet_by_name():
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
    wallet_name = Wallet.objects.first()
    response = client.get(
        f"/api/v1/wallets/{wallet_name}/", HTTP_AUTHORIZATION=token
    )
    assert response.status_code == 200
    assert response.data["name"] == wallet_name.name


@pytest.mark.django_db
def test_wallet_delete():
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
    wallet_name = Wallet.objects.first()
    response = client.delete(
        f"/api/v1/wallets/{wallet_name}/", HTTP_AUTHORIZATION=token
    )
    assert response.status_code == 204
    assert Wallet.objects.count() == 0
