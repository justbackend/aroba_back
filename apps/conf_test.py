import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient
from utils.choices import APIRoutes

USERNAME = "test_user"
PASSWORD = "test_pass"


@pytest.fixture
def get_user():
    hashed_pass = make_password(PASSWORD)
    user, created = get_user_model().objects.get_or_create(
        username=USERNAME, defaults=dict(password=hashed_pass)
    )
    return user


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def login_user(get_user, client):
    response = client.post(f'{APIRoutes.AUTH}login/', {
        'username': get_user.username,
        'password': PASSWORD
    })

    token = response.data['access']
    client.credentials(Authorization=f'Bearer {token}')
    return client
