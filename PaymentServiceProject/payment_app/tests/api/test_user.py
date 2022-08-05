import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_registration_user():
    """Registration test"""
    payload = {
        "username": "harrypotter1988",
        "password": "hogwarts2000",
    }
    response = client.post("/api/v1/registration/users/", payload)
    data = response.data
    assert data["username"] == payload["username"]
    assert response.status_code == 201
    assert User.objects.count() == 1
    assert User.objects.get().username == "harrypotter1988"


@pytest.mark.django_db
def test_login():
    """Login test"""
    payload = {
        "username": "harrypotter1988",
        "password": "hogwarts2000",
    }
    client.post("/api/v1/registration/users/", payload)
    response = client.post("/api/v1/auth/token/login/", payload)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_fail():
    """Login fail test"""
    payload = {
        "username": "notharry1988dasd",
        "password": "hogwarts3012123w",
    }
    response = client.post("/api/v1/auth/token/login/", payload)
    assert response.data == "Not found"


@pytest.mark.django_db
def test_logout():
    """Logout test"""
    payload = {
        "username": "harrypotter1988",
        "password": "hogwarts2000",
    }
    client.post("/api/v1/registration/users/", payload)
    response = client.post("/api/v1/auth/token/login/", payload)
    token_from_response = response.data["auth_token"]
    token = "Token " + str(token_from_response)
    response = client.post(
        "/api/v1/auth/token/logout/", HTTP_AUTHORIZATION=token
    )
    assert response.status_code == 204
