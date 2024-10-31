from django.urls import path
from . import views

urlpatterns = [

    # Dispatcher
    path('new-orders/', views.NewOrdersListView.as_view(), name='new-orders'),
    path('book-order/<int:order_id>/', views.BookOrRollbackOrderView.as_view(), name='book-orders'),

    # create order
    path('create-order/', views.CreateOrderView.as_view(), name='create-order'),



]
