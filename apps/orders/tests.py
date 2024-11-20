import pytest

from apps.conf_test import get_user, login_user, api_client


@pytest.mark.django_db
def test_new_orders(api_client, get_user, login_user):
    print(get_user)
    response = api_client.get(f'/new-orders/')
    print(response)

