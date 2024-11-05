from django.urls import path, include

urlpatterns = [
    path(
        'users/',
        include('apps.users.main.urls'),
        name='users',
    ),

    path(
        'auth/',
        include('apps.users.auth.urls'),
        name='auth',
    ),

    path(
        'orders/',
        include('apps.orders.main.urls'),
        name='orders',
        ),

    path(
        'dispatchers/',
        include('apps.orders.dispatchers.urls'),
        name='dispatchers',
    ),

    path(
        'managers/',
        include('apps.orders.managers.urls'),
        name='managers',
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
    path(
        'checkout/',
        include('apps.checkout.urls'),
        name='checkout',
    ),

]

