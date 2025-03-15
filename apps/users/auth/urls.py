from django.urls import path

from . import views

app_name = 'auth'


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('users/<int:pk>/', views.UpdateUserView.as_view(), name='profile'),

    # my permissions
    path('my-perms/', views.MyPermissionsListAPI.as_view(), name='my-perms'),
]

