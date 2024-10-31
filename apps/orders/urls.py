from django.urls import path
from . import views

urlpatterns = [

    # Dispatcher
    path('new-orders/', views.NewOrdersListView.as_view(), name='new-orders'),

    # create order
    path('create-order/', views.CreateOrderView.as_view(), name='create-order'),

]
