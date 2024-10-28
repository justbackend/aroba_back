from django.contrib import admin
from . import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    class OrderPaymentInline(admin.StackedInline):
        model = models.OrderPayment
        extra = 1

    list_display = ('id', 'code', 'date', 'status', 'total_amount', 'car_number', 'payment_type', 'client')
    list_display_links = ('id', 'code',)
    list_filter = ('date', 'status', 'total_amount', 'car_number', 'payment_type', 'client')


@admin.register(models.OrderPayment)
class OrderPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'type', 'comment', 'order')
    list_display_links = ('id', 'type', 'amount')
    list_filter = ('type', 'order')

