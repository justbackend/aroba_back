from django.urls import path
from . import views


contact_lc = views.ContactViewSet.as_view({'get': 'list', 'post': 'create'})
contact_udd = views.ContactViewSet.as_view({'patch': 'partial_update', 'delete': 'destroy'})

urlpatterns = [

    # imb checkout
    path('checkout-balance/', views.CheckoutBalanceView.as_view(), name='checkout-imb-balance'),
    path('transactions/', views.TransactionsView.as_view(), name='transactions-imb'),
    path('transactions/<int:pk>/', views.UpdateTransactionView.as_view(), name='transactions-imb'),

    # imb contacts
    path('contacs/', contact_lc, name='contacts-imb'),
    path('contacs/<int:id>/', contact_udd, name='contacts-imb'),
]
