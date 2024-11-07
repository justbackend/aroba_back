from django.urls import path
from . import views

urlpatterns = [

    # report orders
    path('report-orders/', views.ReportOrdersListAPI.as_view(), name='report-orders-list'),

    # transactions
    path('transactions/', views.CreateTransactionAPI.as_view(), name='create-transaction'),
    path('transactions/<int:pk>/', views.UpdateTransactionAPI.as_view(), name='update-transaction'),

    # balance and debts
    path('balance-info/', views.BalanceView.as_view(), name='balance'),

]
