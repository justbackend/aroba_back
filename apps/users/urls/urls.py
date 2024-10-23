from django.urls import path
from apps.users import views

urlpatterns = [
    path('salom/', views.SalomView.as_view(), name='salom'),
    path('salom/<int:pk>/', views.SalomView.as_view(), name='salom'),
    path('salom/<str:salom>/<int:id>', views.SalomView.as_view(), name='salom'),
]

