import pytest

from apps.conf_test import get_user, login_user, client
from utils.choices import APIRoutes


@pytest.mark.django_db
def test_new_orders(client, get_user, login_user):
    response = client.get(f'{APIRoutes.DISPATCHERS}new-orders/')

