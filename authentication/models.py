from django.db import models
from django.contrib.auth.models import User

class Dieta(models.Model):
    nombre = models.CharField(max_length=50, null=None)

    def __str__(self):
        return self.nombre
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    dietas = models.ManyToManyField(Dieta)

    def __str__(self):
        return self.user.username