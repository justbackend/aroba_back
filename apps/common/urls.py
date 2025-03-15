from django.urls import path

from . import views

# regions view set
regions_lc = views.RegionViewSet.as_view({'get': 'list', 'post': 'create'})
regions_udd = views.RegionViewSet.as_view({'delete': 'destroy', 'patch': 'partial_update'})

# points view set
points_lc = views.PointViewSet.as_view({'get': 'list', 'post': 'create'})
points_udd = views.PointViewSet.as_view({'delete': 'destroy', 'patch': 'partial_update'})

urlpatterns = [
    # regions
    path('regions/', regions_lc, name='regions_lc'),
    path('regions/<int:pk>/', regions_udd, name='region_udd'),

    # points
    path('points/', points_lc, name='points_lc'),
    path('points/<int:pk>/', points_udd, name='points_udd'),

]
