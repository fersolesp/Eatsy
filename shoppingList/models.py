from authentication.models import Perfil
from django.db import models
from product.models import Producto


class ListaDeCompra(models.Model):
    productos = models.ManyToManyField(Producto)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
