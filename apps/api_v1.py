from django.urls import path, include

urlpatterns = [
    path(
        'users/',
        include('apps.users.urls.base'),
        name='users',
    ),

    path(
        'auth/',
        include('apps.users.urls.auth'),
        name='auth',
    ),

    path(
        'orders/',
        include('apps.orders.urls'),
        name='orders',
        ),

    path(
        'clients/',
        include('apps.clients.urls'),
        name='clients',
        ),

    path(
        'common/',
        include('apps.common.urls'),
        name='common',
    ),

]

