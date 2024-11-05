from django.urls import path
from . import views

urlpatterns = [
    path('report-orders/', views.ReportOrdersListAPI.as_view(), name='report-orders-list'),
]
