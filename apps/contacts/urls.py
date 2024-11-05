from django.urls import path
from . import views


# contacts view set
contacts_lc = views.ContactViewSet.as_view({'get': 'list', 'post': 'create'})
contacts_udd = views.ContactViewSet.as_view({'patch': 'partial_update', 'delete': 'destroy'})


urlpatterns = [
    # contacts
    path('contacts/', contacts_lc, name='contacts-list'),
    path('contacts/<int:pk>/', contacts_udd, name='contacts-detail'),

]
