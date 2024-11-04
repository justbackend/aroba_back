from django.urls import path
from . import views

urlpatterns = [
    # create order
    path('create-order/', views.CreateOrderView.as_view(), name='create-order'),
    path('clients/', views.ClientsListView.as_view(), name='create-order'),

]
