from django.urls import path
from . import views

urlpatterns = [

    # accountant orders
    path('orders/', views.AccountantOrderList.as_view(), name='accountant-orders'),
    path('orders-excel/', views.AccountantOrdersExcel.as_view(), name='accountant-orders'),

    # report orders
    path('finished-orders/', views.FinishedOrders.as_view(), name='accountant-finished-orders')
]
