from django.contrib import admin
from unfold import admin as u_admin
from . import models


@admin.register(models.Contact)
class ContactAdmin(u_admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone')




