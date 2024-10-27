from django.urls import path
from apps.users.views import base as views

app_name = 'users'


# roles
role_lc = views.RoleViewSet.as_view({'get': 'list', 'post': 'create'})
role_udd = views.RoleViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})

# content type
content_type_lc = views.ContentTypeViewSet.as_view({'get': 'list', 'post': 'create'})
content_type_udd = views.ContentTypeViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})

urlpatterns = [

    # roles view set
    path('roles/', role_lc, name='roles'),
    path('roles/<int:pk>/', role_udd, name='roles'),

    # module view set
    path('content-types/', content_type_lc, name='modules'),
    path('content-types/<int:pk>/', content_type_udd, name='modules'),

]
