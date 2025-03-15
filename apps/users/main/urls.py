from django.urls import path

from . import views

app_name = 'users'

# roles
role_udd = views.RoleViewSet.as_view({'patch': 'partial_update', 'delete': 'destroy'})
role_lc = views.RoleViewSet.as_view({'get': 'list', 'post': 'create'})

users_lc = views.UserViewSet.as_view({'get': 'list', 'post': 'create'})
users_udd = views.UserViewSet.as_view({'patch': 'partial_update', 'delete': 'destroy'})

sections_lc = views.SectionViewSet.as_view({'get': 'list'})

urlpatterns = [

    # roles view set
    path('roles/', role_lc, name='roles'),
    path('roles/<int:pk>/', role_udd, name='roles'),

    # users
    path('users/', users_lc, name='users'),
    path('users/<int:pk>/', users_udd, name='users'),

    # sections
    path('sections/', sections_lc, name='sections'),

]
