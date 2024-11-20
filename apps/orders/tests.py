from apps.conf_test import *
from utils.choices import APIRoutes
import pytest


@pytest.mark.django_db
def test_new_orders(auth_client):
    response = auth_client.get(f'{APIRoutes.DISPATCHERS}new-orders/')

    assert response.status_code == 200



