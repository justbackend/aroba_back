from django.db import models

from apps.common.models import BaseModel
from . import managers
from utils import choices


class Client(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Client name")
    phone = models.CharField(max_length=20, verbose_name="Client phone")
    requisite = models.CharField(max_length=255, verbose_name="Requisite comment")
    requisite_file = models.FileField(upload_to="clients/", verbose_name="Requisite file")
    accounting_phone = models.CharField(max_length=20, verbose_name="Account phone number")
    deleted = models.BooleanField(default=False, verbose_name="Deleted")

    active_objects = managers.ActiveClientManager()

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        db_table = "clients"

    def __str__(self):
        return self.name


class ClientRoute(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    type = models.CharField(
        max_length=15,
        verbose_name="Route type",
        choices=choices.ClientRouteTypes.choices,
        default=choices.ClientRouteTypes.CASH
    )
    loading = models.ForeignKey(
        'common.Point',
        on_delete=models.PROTECT,
        verbose_name="Loading",
        related_name="client_routes_loading",
    )
    unloading = models.ForeignKey(
        'common.Point',
        on_delete=models.PROTECT,
        verbose_name="Loading",
        related_name="client_routes_unloading",
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name="Client",
        related_name="routes",
    )

    class Meta:
        verbose_name = "Client route"
        verbose_name_plural = "Client routes"
        db_table = "clients_route"

    def __str__(self):
        return str(self.client)
