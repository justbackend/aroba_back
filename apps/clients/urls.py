from django.urls import path
from . import views


# clients view set
clients_lc = views.ClientViewSet.as_view({'get': 'list', 'post': 'create'})
clients_udd = views.ClientViewSet.as_view({'patch': 'partial_update', 'delete': 'destroy'})


# routes view set
routes_lc = views.ClientRouteViewSet.as_view({'get': 'list', 'post': 'create'})
routes_udd = views.ClientRouteViewSet.as_view({'patch': 'partial_update', 'delete': 'destroy'})

urlpatterns = [
    path('', clients_lc, name='client_lc'),
    path('<int:pk>/', clients_udd, name='client_udd'),

    path('routes/', routes_lc, name='client_routes'),
    path('routes/<int:pk>/', routes_udd, name='client_routes_udd'),

    # for order create client routes
    path('create-order-routes/<int:client_id>/', views.CombinationCreateOrderRoutesListAPI.as_view(), name='c-routes'),
]

