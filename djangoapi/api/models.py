from django.db import models
from django.contrib.auth.models import User  # Importa el modelo de usuario

class cliente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario
    nombre = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class mesa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    numero_mesa = models.IntegerField()
    capacidad = models.PositiveIntegerField()

    def __str__(self):
        return f"Mesa {self.numero_mesa} - Capacidad {self.capacidad}"

class reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    cliente = models.ForeignKey(cliente, on_delete=models.CASCADE)
    mesa = models.ForeignKey(mesa, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reserva de {self.cliente} para la Mesa {self.mesa.numero_mesa} el {self.fecha} a las {self.hora}"
