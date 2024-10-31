from django.urls import path
from . import views


urlpatterns = [
    path('new-orders/', views.NewOrdersListView.as_view(), name='new-orders'),

    path('book-order/<int:order_id>/', views.BookOrRollbackOrderView.as_view(), name='book-orders'),

    path('filling-orders/', views.FillingOrdersListView.as_view(), name='filling-orders'),
]

