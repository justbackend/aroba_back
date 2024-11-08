from django.urls import path
from . import views

urlpatterns = [

    # accountant orders
    path('clients/', views.TransClientsViewList.as_view(), name='accountant-orders'),

    # report orders
    path('finished-orders/', views.FinishedOrders.as_view(), name='accountant-finished-orders'),
    path('finished-orders-excel/', views.FinishedOrdersExcel.as_view(), name='accountant-finished-orders-excel'),
]
