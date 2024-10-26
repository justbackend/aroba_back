from django.urls import path
from apps.users.views import auth as views

app_name = 'auth'


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
]

