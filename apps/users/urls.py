from django.urls import path
from . import views

urlpatterns = [
    path('salom/', views.SalomView.as_view(), name='salom'),
]

