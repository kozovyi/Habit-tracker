import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client():
    api_client = APIClient()
    payload = {
        "email": "pablo@gmail.com",
        "password": "gfdlk2005"
    }
    User.objects.create_user(username="pablo", **payload)
    response = api_client.post("/api/v1/auth/token/jwt/create/", payload)
    access_token = response.data.get("access", None)
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    return api_client

@pytest.fixture
def auth_client_another():
    api_client = APIClient()
    payload = {
        "email": "dmitro@gmail.com",
        "password": "gfdlk2005"
    }
    User.objects.create_user(username="dmitro", **payload)
    response = api_client.post("/api/v1/auth/token/jwt/create/", payload)
    access_token = response.data.get("access", None)
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    return api_client