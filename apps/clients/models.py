from django.db import models
from apps.common.models import BaseModel


class Client(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Client name")
    phone = models.CharField(max_length=20, verbose_name="Client phone")
    requisite = models.CharField(max_length=255, verbose_name="Requisite comment")
    requisite_file = models.FileField(upload_to="clients/", verbose_name="Requisite file")
    accounting_phone = models.CharField(max_length=20, verbose_name="Account phone number")

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        db_table = "clients"


class ClientRoute(BaseModel):
    amount = ...
    loading = ...
    unloading = ...
    client = ...

    class Meta:
        verbose_name = "Client route"
        verbose_name_plural = "Client routes"
        db_table = "clients_route"




