from django.urls import path
from . import views


# clients view set
clients_lc = views.ClientViewSet.as_view({'get': 'list', 'post': 'create'})
clients_udd = views.ClientViewSet.as_view({'patch': 'partial_update', 'delete': 'destroy'})

urlpatterns = [
    path('', clients_lc, name='client_lc'),
    path('<int:pk>/', clients_udd, name='client_udd'),

    # for order create client routes
    path('create-order-routes/', views.CreateOrderRoutes.as_view(), name='create_order_routes'),
]

