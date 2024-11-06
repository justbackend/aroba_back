from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.AccountantOrderList.as_view(), name='accountant-orders'),
]
