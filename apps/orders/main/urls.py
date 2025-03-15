from django.urls import path

from . import views

urlpatterns = [

    # create order
    path('create-order/', views.CreateOrderView.as_view(), name='create-order'),
    path('clients/', views.ClientsListView.as_view(), name='create-order'),
    path('create-order-routes/<int:client_id>/', views.CombinationCreateOrderRoutesListAPI.as_view(), name='c-routes'),

]
