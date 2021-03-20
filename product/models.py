from django.db import models
from authentication.models import Perfil
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Ubicacion(models.Model):
    nombre = models.CharField(max_length=200, null=None)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, validators=[
                                  MinValueValidator(-90), MaxValueValidator(90)],null=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, validators=[
                                   MinValueValidator(-180), MaxValueValidator(180)],null=True)
    @property
    def esSupermercado(self):
        if(self.latitud == None and self.longitud == None):
            True
        else:
            False


class Producto(models.Model):
    Dieta_Enum = (
        ('Vegano', 'Vegano'),
        ('Vegetariano', 'Vegetariano'),
        ('Gluten', 'Gluten'),
        ('Lactosa', 'Lactosa'),
        ('Marisco', 'Marisco'),
        ('Frutos secos', 'Frutos secos'),
    )
    State_Enum = (("Pendiente", "Pendiente de Revisión"),
                  ("Aceptado", "Aceptado"))
    titulo = models.CharField(max_length=100, null=None)
    descripcion = models.TextField(null=None)
    fecha = models.DateTimeField(auto_now=True)
    foto = models.TextField()
    precioMedio = models.DecimalField(
        null=None,max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    dietas = models.CharField(max_length=12, choices=Dieta_Enum,
                              default='Vegetariano', blank=False, verbose_name="Dieta")
    estado = models.CharField(max_length=9, choices=State_Enum,
                              default='Pendiente', blank=False, verbose_name="Estado")
    user = models.ForeignKey(Perfil, on_delete=models.DO_NOTHING)
    ubicaciones = models.ManyToManyField(
        Ubicacion, through="UbicacionProducto")


class UbicacionProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(Perfil, on_delete=models.DO_NOTHING)
    precio = models.DecimalField(
        null=None, max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])