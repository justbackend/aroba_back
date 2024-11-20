# tests/conf_test.py

import pytest
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

USERNAME = "test_user"
PASSWORD = "test_pass"


@pytest.fixture
def get_user():
    """
    Yangi foydalanuvchi yaratish uchun fixture.
    """
    hashed_pass = make_password(PASSWORD)
    user = get_user_model().objects.get_or_create(
        username=USERNAME, defaults=dict(password=hashed_pass)
    )
    return user


@pytest.fixture
def api_client():
    """
    APIClient fixture.
    """
    return APIClient()


@pytest.fixture
def login_user(get_user, api_client):
    """
    Foydalanuvchini tizimga kirgan holda qaytarish.
    """
    response = api_client.post('/api/v1/auth/login/', {
        'username': get_user.username,
        'password': PASSWORD
    })
    token = response.data['access']  # tokenni olish (JWT)
    api_client.credentials(Authorization=f'Bearer {token}')
    return api_client
