from django.urls import path
from . import views

urlpatterns = [

    # report orders
    path('report-orders/', views.ReportOrdersListAPI.as_view(), name='report-orders-list'),

    # create transactions
    path('create-transaction/', views.CreateTransactionAPI.as_view(), name='create-transaction'),

    # transactions
    path('transactions/', views.TransactionListAPI.as_view(), name='create-transaction'),

]
