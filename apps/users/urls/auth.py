from django.urls import path
from apps.users import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
]

