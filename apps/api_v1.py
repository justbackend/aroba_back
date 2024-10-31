from django.urls import path, include

urlpatterns = [
    path(
        'users/',
        include('apps.users.urls.users'),
        name='users',
    ),

    path(
        'auth/',
        include('apps.users.urls.auth'),
        name='auth',
    ),

    path(
        'orders/',
        include('apps.orders.urls.orders'),
        name='orders',
        ),
    path(
        'dispatchers/',
        include('apps.orders.urls.dispatchers'),
        name='dispatchers',
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

