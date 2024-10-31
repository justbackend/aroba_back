from django.urls import path
from .. views import orders as views

urlpatterns = [
    # create order
    path('create-order/', views.CreateOrderView.as_view(), name='create-order'),

]
