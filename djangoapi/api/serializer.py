from rest_framework import serializers
from .models import cliente, mesa, reserva

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = cliente
        fields = ['id', 'nombre', 'email', 'telefono']

class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = mesa
        fields = ['id', 'numero_mesa', 'capacidad']

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = reserva
        fields = ['id', 'fecha', 'hora', 'cliente', 'mesa']
