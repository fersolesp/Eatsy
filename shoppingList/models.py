from django.db import models
from authentication.models import Perfil
from product.models import Producto

class ListaDeCompra(models.Model):
    productos = models.ManyToManyField(Producto)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
