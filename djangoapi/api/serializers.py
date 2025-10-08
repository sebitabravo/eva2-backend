from rest_framework import serializers
from .models import Cliente, Mesa, Reserva
from django.utils import timezone
import re


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'email', 'telefono', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_email(self, value):
        """Valida formato de email"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Formato de email inválido")
        
        # Validar unicidad por usuario
        clean_email = value.lower()
        user = self.context['request'].user
        
        # Al crear
        if not self.instance:
            if Cliente.objects.filter(usuario=user, email=clean_email).exists():
                raise serializers.ValidationError("Ya existe un cliente con este email")
        # Al actualizar
        else:
            if Cliente.objects.filter(usuario=user, email=clean_email).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Ya existe un cliente con este email")
        
        return clean_email

    def validate_telefono(self, value):
        """Valida formato de teléfono chileno"""
        # Permite formatos: +56912345678, 912345678, 221234567
        phone_regex = r'^(\+?56)?[2-9]\d{8}$'
        clean_phone = re.sub(r'[\s\-\(\)]', '', value)
        if not re.match(phone_regex, clean_phone):
            raise serializers.ValidationError("Formato de teléfono inválido. Use formato chileno.")
        return clean_phone

    def validate_nombre(self, value):
        """Valida que el nombre tenga al menos 2 caracteres"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("El nombre debe tener al menos 2 caracteres")
        return value.strip()


class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesa
        fields = ['id', 'numero_mesa', 'capacidad', 'activa', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_numero_mesa(self, value):
        """Valida que el número de mesa sea positivo y único por usuario"""
        if value <= 0:
            raise serializers.ValidationError("El número de mesa debe ser mayor a 0")

        # Verifica unicidad por usuario al crear
        if not self.instance:
            user = self.context['request'].user
            if Mesa.objects.filter(usuario=user, numero_mesa=value).exists():
                raise serializers.ValidationError(f"Ya existe una mesa con el número {value}")

        return value

    def validate_capacidad(self, value):
        """Valida que la capacidad esté entre 1 y 20 personas"""
        if value < 1:
            raise serializers.ValidationError("La capacidad debe ser al menos 1 persona")
        if value > 20:
            raise serializers.ValidationError("La capacidad máxima es 20 personas")
        return value


class ReservaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    mesa_numero = serializers.IntegerField(source='mesa.numero_mesa', read_only=True)

    class Meta:
        model = Reserva
        fields = ['id', 'fecha', 'hora', 'cliente', 'mesa', 'cliente_nombre', 'mesa_numero', 'estado', 'notas', 'created_at', 'updated_at']
        read_only_fields = ['id', 'cliente_nombre', 'mesa_numero', 'created_at', 'updated_at']

    def validate_fecha(self, value):
        """Valida que la fecha de reserva no sea en el pasado"""
        if value < timezone.now().date():
            raise serializers.ValidationError("No se pueden hacer reservas en fechas pasadas")

        # Límite de 90 días en el futuro
        max_date = timezone.now().date() + timezone.timedelta(days=90)
        if value > max_date:
            raise serializers.ValidationError("No se pueden hacer reservas con más de 90 días de anticipación")

        return value

    def validate_hora(self, value):
        """Valida que la hora de reserva esté en horario de atención"""
        hour = value.hour
        minute = value.minute

        # Horario: 12:00 - 23:00
        if hour < 12 or hour >= 23:
            raise serializers.ValidationError("El horario de atención es de 12:00 a 23:00")

        # Solo acepta reservas cada 30 minutos
        if minute not in [0, 30]:
            raise serializers.ValidationError("Las reservas solo se aceptan cada 30 minutos (ej: 12:00, 12:30)")

        return value

    def validate(self, data):
        """Validaciones cruzadas"""
        fecha = data.get('fecha')
        hora = data.get('hora')
        mesa_obj = data.get('mesa')
        cliente_obj = data.get('cliente')
        user = self.context['request'].user

        # Verifica que cliente y mesa pertenezcan al usuario
        if cliente_obj and cliente_obj.usuario != user:
            raise serializers.ValidationError({"cliente": "El cliente seleccionado no le pertenece"})

        if mesa_obj and mesa_obj.usuario != user:
            raise serializers.ValidationError({"mesa": "La mesa seleccionada no le pertenece"})

        # Verifica disponibilidad de mesa (no al editar la misma reserva)
        if fecha and hora and mesa_obj:
            reservas_existentes = Reserva.objects.filter(
                fecha=fecha,
                hora=hora,
                mesa=mesa_obj
            ).exclude(estado='cancelada')

            # Si estamos editando, excluir la reserva actual
            if self.instance:
                reservas_existentes = reservas_existentes.exclude(pk=self.instance.pk)

            if reservas_existentes.exists():
                raise serializers.ValidationError({
                    "mesa": f"La mesa {mesa_obj.numero_mesa} ya está reservada para {fecha} a las {hora}"
                })

        return data
