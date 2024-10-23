from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('salom/', views.SalomView.as_view(), name='salom'),
    path('salom/<int:pk>/', views.SalomView.as_view(), name='salom'),
    path('salom/<str:salom>/<int:id>', views.SalomView.as_view(), name='salom'),
]

