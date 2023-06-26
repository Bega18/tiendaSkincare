from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=25)
    precio = models.IntegerField(null=True)
    existencia = models.IntegerField(null=True)
    imagen = models.ImageField(upload_to='images/')

    def __str__(self):
        return '{0},{1},{2}'. format(self.nombre, self.precio, self.existencia)

class Cliente(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    direccion = models.CharField(max_length=100)
    def __str__(self):
        return '{0},{1},{2}'.format(self.nombre, self.apellido, self.direccion)