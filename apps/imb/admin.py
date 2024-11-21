from django.contrib import admin
from unfold import admin as u_admin
from . import models


@admin.register(models.IMBCheckout)
class IMBCheckoutAdmin(u_admin.ModelAdmin):
    list_display = ('id', 'balance',)
