from django.urls import path
from . import views

app_name = 'users'


# roles
role_lc = views.RoleViewSet.as_view({'get': 'list', 'post': 'create'})
role_udd = views.RoleViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})

# modules
module_lc = views.ModuleViewSet.as_view({'get': 'list', 'post': 'create'})
module_udd = views.ModuleViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})

urlpatterns = [

    # roles view set
    path('roles/', role_lc, name='roles'),
    path('roles/<int:pk>/', role_udd, name='roles'),

    # module view set
    path('modules/', module_lc, name='modules'),
    path('modules/<int:pk>/', module_udd, name='modules'),

]
