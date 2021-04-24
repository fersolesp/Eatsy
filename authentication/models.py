from django.db import models
from django.contrib.auth.models import User

class Dieta(models.Model):
    nombre = models.CharField(max_length=50, null=None)
    logo = models.CharField(max_length=100, default="")

    def __str__(self):

        "Devuelve el nombre de la dieta"
        return self.nombre
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    dietas = models.ManyToManyField(Dieta)
    activeAccount = models.BooleanField(blank=False, null=False, default=False)

    def __str__(self):
        return self.user.username