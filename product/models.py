from authentication.models import Perfil
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Ubicacion(models.Model):
    nombre = models.CharField(max_length=200, null=None)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, validators=[
                                  MinValueValidator(-90), MaxValueValidator(90)],null=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, validators=[
                                   MinValueValidator(-180), MaxValueValidator(180)],null=True)
                                   
    @property
    def esSupermercado(self):
        return self.latitud == None and self.longitud == None
        
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
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    causa = CausaReporte._meta.get_field('causa')
    comentarios = models.TextField(null=False, blank=False)

    State_Enum = (("Pendiente", "Pendiente de Revisión"),
            ("Resuelto", "Resuelto"),
            ("No procede","No procede"))

    estado = models.CharField( choices=State_Enum,
                              default='Pendiente', blank=False, verbose_name="Estado")

    # Más antiguos primero
    class Meta:
        ordering = ['id']

    def __str__(self):
        return '{} ({})'.format(self.producto.titulo, self.causa)

class Valoracion(models.Model):
    puntuacion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Perfil, on_delete=models.DO_NOTHING)
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.producto.titulo + ': ' +str(self.puntuacion)

class Aportacion(models.Model):
    titulo = models.CharField(max_length=100,null=False,blank=False)
    mensaje = models.TextField(max_length=1000,null=False,blank=False)
    fecha = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Perfil, on_delete=models.DO_NOTHING)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class ChangeRequest(models.Model):
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    dietas = models.ManyToManyField(Dieta)

    creation_date = models.DateTimeField(auto_now_add=True)
    creation_user = models.ForeignKey(User, null=False, on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        # Borrar peticiones de cambio anteriores del mismo usuario y producto
        ChangeRequest.objects.filter(product__id=self.product.id, creation_user__id=self.creation_user.id).exclude(id=self.id).delete()

        super(ChangeRequest, self).save(*args, **kwargs)
    
    def apply(self):
        self.product.dietas.set(self.dietas.all())
        self.product.save()

        self.delete()

    def __str__(self):
        return self.product.titulo

    # Más antiguos primero
    class Meta:
        ordering = ['id']