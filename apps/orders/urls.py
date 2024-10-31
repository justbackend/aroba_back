from django.urls import path
from . import views

urlpatterns = [

    # Dispatcher
    path('new-orders/', views.NewOrdersListView.as_view(), name='new-orders'),

]
