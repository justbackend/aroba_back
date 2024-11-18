from django.db import models

from utils.base import BaseModel
from . import managers
from utils import choices
import utils


class Client(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Client name")
    phone = models.CharField(max_length=20, verbose_name="Client phone", validators=[utils.PhoneValidator()])
    requisite = models.CharField(max_length=255, verbose_name="Requisite comment", null=True, blank=True)
    requisite_file = models.FileField(upload_to="clients/", verbose_name="Requisite file", null=True, blank=True)
    deleted = models.BooleanField(default=False, verbose_name="Deleted")
    inn = models.CharField(max_length=15, verbose_name="Inner client", null=True, blank=True)
    customer = models.CharField(max_length=255, verbose_name="Customer", null=True, blank=True)
    type = models.CharField(
        max_length=15,
        verbose_name="Route type",
        choices=choices.ClientRouteTypes.choices,
        default=choices.ClientRouteTypes.CASH
    )
    accounting_phone = models.CharField(
        max_length=20, verbose_name="Accounting phone number",
        validators=[utils.PhoneValidator()], null=True, blank=True
    )

    objects = utils.Manager()
    active_objects = managers.ActiveClientManager()

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        db_table = "clients"

    def __str__(self):
        return self.name


class ClientRoute(BaseModel):
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Amount")
    loading = models.ForeignKey(
        'common.Point',
        on_delete=models.PROTECT,
        verbose_name="Loading",
        related_name="client_routes_loading",
    )
    unloading = models.ForeignKey(
        'common.Point',
        on_delete=models.PROTECT,
        verbose_name="UnLoading",
        related_name="client_routes_unloading",
    )
    client = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        verbose_name="Client",
        related_name="routes",
    )

    class Meta:
        verbose_name = "Client route"
        verbose_name_plural = "Client routes"
        db_table = "clients_route"
        constraints = [
            models.UniqueConstraint(fields=["loading", "unloading", 'client'], name="unique_client_router"),
        ]

    def __str__(self):
        return str(self.client)
