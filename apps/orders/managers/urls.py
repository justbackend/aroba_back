from django.urls import path

from . import views

urlpatterns = [
    path('additional-amount/<int:order_id>/', views.AdditionalAmountView.as_view(), name='additional-amount'),
]

