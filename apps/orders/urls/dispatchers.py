from django.urls import path
from ..views import dispatchers as views


urlpatterns = [
    path('new-orders/', views.NewOrdersListView.as_view(), name='new-orders'),
    path('book-order/<int:order_id>/', views.BookOrRollbackOrderView.as_view(), name='book-orders'),
]

