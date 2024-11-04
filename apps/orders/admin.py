from django.contrib import admin
from unfold import admin as u_admin
from . import models


@admin.register(models.Order)
class OrderAdmin(u_admin.ModelAdmin):
    class OrderPaymentInline(u_admin.StackedInline):
        model = models.OrderPayment
        extra = 1

    class OrderLogInline(u_admin.StackedInline):
        model = models.OrderLog
        extra = 1

    list_display = ('id', 'code', 'date', 'status', 'total_amount', 'car_number', 'payment_type', 'client')
    list_display_links = ('id', 'code',)
    list_filter = ('date', 'status', 'total_amount', 'car_number', 'payment_type', 'client')
    inlines = (OrderPaymentInline, OrderLogInline)


@admin.register(models.OrderPayment)
class OrderPaymentAdmin(u_admin.ModelAdmin):
    list_display = ('id', 'amount', 'type', 'comment', 'order')
    list_display_links = ('id', 'type', 'amount')
    list_filter = ('type', 'order')
