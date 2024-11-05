from django.urls import path
from . import views

urlpatterns = [

    # report orders
    path('report-orders/', views.ReportOrdersListAPI.as_view(), name='report-orders-list'),

    # transactions
    path('transactions/', views.CreateTransactionAPI.as_view(), name='create-transaction'),

]
