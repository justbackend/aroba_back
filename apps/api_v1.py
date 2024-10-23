from django.urls import path, include

urlpatterns = [
    path(
        'users/',
        include('apps.users.urls.urls'),
        name='users'
    ),
    path(
        'auth/',
        include('apps.users.urls.auth'),
        name='auth'
    ),

]

