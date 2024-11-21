from django.contrib import admin
from unfold import admin as u_admin
from unfold.contrib.inlines.admin import NonrelatedTabularInline
from . import models


class IMBTransactionsInline(NonrelatedTabularInline):
    model = models.IMBTransaction
    extra = 0

    def get_form_queryset(self, obj):
        """
        Gets all nonrelated objects needed for inlines. Method must be implemented.
        """
        return self.model.objects.all()

    def save_new_instance(self, parent, instance):
        """
        Extra save method which can for example update inline instances based on current
        main model object. Method must be implemented.
        """
        pass


@admin.register(models.IMBCheckout)
class IMBCheckoutAdmin(u_admin.ModelAdmin):
    list_display = ('id', 'balance',)


@admin.register(models.IMBTransaction)
class IMBTransactionAdmin(u_admin.ModelAdmin):
    list_display = ('id', 'amount', 'comment', 'type')
