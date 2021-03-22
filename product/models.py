from django.db import models
from authentication.models import Perfil
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

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

    def __str__(self):
        return self.nombre

class Dieta(models.Model):
    nombre = models.CharField(max_length=50, null=None)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    State_Enum = (("Pendiente", "Pendiente de Revisión"),
                  ("Aceptado", "Aceptado"))

    titulo = models.CharField(max_length=100, null=None)
    descripcion = models.TextField(null=None)
    fecha = models.DateTimeField(auto_now=True)
    foto = models.TextField()
    precioMedio = models.DecimalField(
        null=None,max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    dietas = models.ManyToManyField(Dieta)
    estado = models.CharField(max_length=9, choices=State_Enum,
                              default='Pendiente', blank=False, verbose_name="Estado")
    user = models.ForeignKey(Perfil, on_delete=models.DO_NOTHING)
    ubicaciones = models.ManyToManyField(
        Ubicacion, through="UbicacionProducto")

    # Por defecto se ordena por id descendiente (más nuevos primero)
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.titulo

class UbicacionProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(Perfil, on_delete=models.DO_NOTHING)
    precio = models.DecimalField(
        null=None, max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.ubicacion.nombre

class CausaReporte(models.Model):
    causa = models.CharField(max_length=160, null=False, blank=False)

    def __str__(self):
        return self.causa

class Reporte(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    causa = CausaReporte._meta.get_field('causa')
    comentarios = models.TextField(null=False, blank=False)

    # Más antiguos primero
    class Meta:
        ordering = ['id']

    def __str__(self):
        return '{} ({})'.format(self.producto.titulo, self.causa)