import pytest

from rest_framework import status
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_add_activity_unauthorized(api_client):
    payload = {
        "name": "Reading",
        "descriprion": "Read every day 5 min.",
        "is_archived": False
    }

    response = api_client.post("/api/v1/activity/", payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_add_activity(auth_client):
    payload = {
        "name": "Reading",
        "descriprion": "Read every day 5 min.",
        "is_archived": False
    }
    response = auth_client.post("/api/v1/activity/", payload)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_activity_invalid_data(auth_client):
    payload = {
        "descriprion": "Read every day 5 min.",
        "is_archived": False
    }
    response = auth_client.post("/api/v1/activity/", payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_retrieve_other_user_activity(auth_client, auth_client_another):
    payload = {
        "name": "Reading",
        "descriprion": "Read every day 5 min.",
        "is_archived": False
    }

    response_activity = auth_client.post("/api/v1/activity/", payload)

    assert response_activity.status_code == status.HTTP_201_CREATED
    
    pk = response_activity.data["pk"]
    response_ok = auth_client.get(f"/api/v1/activity/{pk}/")
    response_err = auth_client_another.get(f"/api/v1/activity/{pk}/")

    assert response_ok.status_code == status.HTTP_200_OK
    assert response_err.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_get_activity_list_isolation(auth_client, auth_client_another):
    payload_1 = {
        "name": "Reading (User 1)",
        "description": "User 1 activity",
        "is_archived": False
    }
    payload_2 = {
        "name": "Gym (User 2)",
        "description": "User 2 activity",
        "is_archived": False
    }
    
    auth_client.post("/api/v1/activity/", payload_1)
    auth_client_another.post("/api/v1/activity/", payload_2)
    response_1 = auth_client.get("/api/v1/activity/")
    response_2 = auth_client_another.get("/api/v1/activity/")

    assert response_1.status_code == status.HTTP_200_OK
    assert len(response_1.data) == 1
    assert response_1.data[0]["name"] == "Reading (User 1)"
    assert response_2.status_code == status.HTTP_200_OK
    assert len(response_2.data) == 1
    assert response_2.data[0]["name"] == "Gym (User 2)"