from django.urls import path, include

urlpatterns = [
    path(
        'users/',
        include('apps.users.base.urls'),
        name='users'
    ),
    path(
        'auth/',
        include('apps.users.auth.urls'),
        name='auth'
    ),
    path(
        'orders/',
        include('apps.orders.urls'),
        name='orders'
        ),
    path(
        'clients/',
        include('apps.clients.urls'),
        name='clients'
        ),
    path(
        'common/',
        include('apps.common.urls'),
        name='common'
    ),

]

