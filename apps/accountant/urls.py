from django.urls import path
from . import views

urlpatterns = [

    # accountant orders
    path('clients/', views.TransClientsViewList.as_view(), name='accountant-clients-list'),
    path('clients/<int:pk>/', views.TransClientsViewUpdate.as_view(), name='accountant-clients-list'),
    path('clients-excel/', views.TransClientsViewExcel.as_view(), name='accountant-clients-excel'),

    # summary orders
    path('finished-orders/', views.FinishedOrders.as_view(), name='accountant-finished-orders'),
    path('finished-orders-excel/', views.FinishedOrdersExcel.as_view(), name='accountant-finished-orders-excel'),

    # invoice orders
    path('invoice-orders/', views.InvoiceOrders.as_view(), name='accountant-invoices'),
    path('create-invoice/', views.CreateInvoice.as_view(), name='accountant-invoices-create'),
    path('update-invoice/<int:pk>/', views.UpdateInvoice.as_view(), name='accountant-invoices-update'),
]
