from django.urls import path
from . import views

urlpatterns = [

    # accountant orders
    path('clients/', views.TransClientsViewList.as_view(), name='accountant-clients-list'),
    path('clients/<int:pk>/', views.TransClientsViewUpdate.as_view(), name='accountant-clients-list'),
    path('clients-excel/', views.TransClientsViewExcel.as_view(), name='accountant-clients-excel'),

    # report orders
    path('finished-orders/', views.FinishedOrders.as_view(), name='accountant-finished-orders'),
    path('finished-orders-excel/', views.FinishedOrdersExcel.as_view(), name='accountant-finished-orders-excel'),

    # invoice orders
    path('invoice-oredrs/', views.Invoices.as_view(), name='accountant-invoices'),
]
