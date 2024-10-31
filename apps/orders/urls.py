from django.urls import path
from . import views

urlpatterns = [
    path('new-orders/', views.NewOrdersListView.as_view(), name='new-orders'),

]
