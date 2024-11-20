import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from utils.choices import APIRoutes

USERNAME = "test_user"
PASSWORD = "test_pass"


@pytest.fixture
def get_user():
    hashed_pass = make_password(PASSWORD)
    user, created = get_user_model().objects.get_or_create(
        username=USERNAME, defaults=dict(password=hashed_pass, is_superuser=True, is_staff=True)
    )

    return user


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def auth_client(get_user, api_client):
    response = api_client.post(f'{APIRoutes.AUTH}login/', {
        'username': get_user.username,
        'password': PASSWORD
    })

    assert response.status_code == 200, f"Login failed: {response.data}"
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client

