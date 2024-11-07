from django.urls import path

from . import views

urlpatterns = [

    # additional amount
    path('additional-amount/<int:order_id>/', views.AdditionalAmountView.as_view(), name='additional-amount'),

    # orders status
    path('status-orders/', views.StatusOrdersListView.as_view(), name='status-orders'),
    path('status-orders/<int:pk>/', views.UpdateOrderStatusView.as_view(), name='status-orders-update'),

    # delete and rollback order
    path('delete-order/<int:order_id>/', views.DeleteOrderStatusView.as_view(), name='status-orders-update'),
    path('rollback-order/<int:order_id>/', views.RollbackOrderView.as_view(), name='status-orders'),

]

