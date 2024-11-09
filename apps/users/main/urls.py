from django.urls import path
from . import views

app_name = 'users'


# roles
role_lc = views.RoleViewSet.as_view({'get': 'list', 'post': 'create'})
role_udd = views.RoleViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})

# content type
modules_lc = views.ModuleViewSet.as_view({'get': 'list', 'post': 'create'})
modules_udd = views.ModuleViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})


users_lc = views.UserViewSet.as_view({'get': 'list', 'post': 'create'})
users_udd = views.UserViewSet.as_view({'patch': 'partial_update', 'delete': 'destroy'})

urlpatterns = [

    # roles view set
    path('roles/', role_lc, name='roles'),
    path('roles/<int:pk>/', role_udd, name='roles'),

    # module view set
    path('modules/', modules_lc, name='modules'),
    path('modules/<int:pk>/', modules_udd, name='modules'),

    # users
    path('users/', users_lc, name='users'),
    path('users/<int:pk>/', users_udd, name='users'),

]
