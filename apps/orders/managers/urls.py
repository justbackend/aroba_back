from django.urls import path

from . import views

urlpatterns = [
    path('additional-amount/<int:order_id>/', views.AdditionalAmountView.as_view(), name='additional-amount'),
    path('status-orders/', views.StatusOrdersListView.as_view(), name='status-orders'),
    path('rollback-order/<int:order_id>/', views.RollbackOrderView.as_view(), name='status-orders'),
    path('status-orders/<int:pk>/', views.UpdateOrderStatusView.as_view(), name='status-orders'),
]

