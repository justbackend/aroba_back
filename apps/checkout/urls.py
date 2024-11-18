from django.urls import path
from . import views

urlpatterns = [

    # report orders
    path('report-orders/', views.ReportOrdersListAPI.as_view(), name='report-orders-list'),
    path('pay-order/<int:order_id>/', views.PayOrder.as_view(), name='pay-cash-order'),
    path('pay-cleint-order/<int:order_id>/', views.PayClientOrder.as_view(), name='pay-cash-order'),

    # transactions
    path('transactions/', views.CreateTransactionAPI.as_view(), name='create-transaction'),
    path('transactions-excel/', views.TransactionsExcel.as_view(), name='create-transaction'),
    path('transactions/<int:pk>/', views.UpdateTransactionAPI.as_view(), name='update-transaction'),

    # balance and debts
    path('balance-info/', views.BalanceView.as_view(), name='balance'),

    # chash summary
    path('cash-summary/', views.CashSummaryListView.as_view(), name='checkout'),
    path('cash-summary-excel/', views.CashSummaryExcelView.as_view(), name='checkout'),

]
