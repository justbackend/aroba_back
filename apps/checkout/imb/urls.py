from django.urls import path
from . import views


urlpatterns = [
    path('checkout-balance/', views.CheckoutBalanceView.as_view(), name='checkout-imb-balance'),
    path('transactions/', views.TransactionsView.as_view(), name='transactions-imb'),
    path('transactions/<int:pk>/', views.UpdateTransactionView.as_view(), name='transactions-imb'),
]
