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
    path('contacts/', contact_lc, name='contacts-imb'),
    path('contacts/<int:pk>/', contact_udd, name='contacts-imb'),


    # send contact to telegram
    path('send-contact/<int:phone>/', views.SendToTelegramView.as_view(), name='send-contact'),

]
