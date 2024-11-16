from django.urls import path
from . import views

urlpatterns = [
    # new orders
    path('new-orders/', views.NewOrdersListView.as_view(), name='new-orders'),

    # book order
    path('book-order/<int:order_id>/', views.BookOrRollbackOrderView.as_view(), name='book-orders'),

    # filling orders
    path('filling-orders/', views.FillingOrdersListView.as_view(), name='filling-orders'),
    path('fill-order/<int:order_id>/', views.FillingOrderView.as_view(), name='filling-orders'),

]

