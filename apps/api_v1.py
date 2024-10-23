from django.urls import path, include

urlpatterns = [
    path(
        'users/',
        include('apps.users.common.urls'),
        name='users'
    ),
    path(
        'auth/',
        include('apps.users.auth.urls'),
        name='auth'
    ),

]

