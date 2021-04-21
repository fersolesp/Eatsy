from django.db import models
from authentication.models import Perfil
from product.models import Producto

class Receta(models.Model):
    nombre = models.CharField(max_length=100, null=None)
    imagen = models.ImageField(upload_to='photos')
    descripcion = models.TextField(null=None)
    productos = models.ManyToManyField(Producto)
    perfil = models.ForeignKey(Perfil, on_delete=models.DO_NOTHING)
