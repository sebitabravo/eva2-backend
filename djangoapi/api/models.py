from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta


class Cliente(models.Model):
    """
    Modelo de Cliente - Representa a los clientes del restaurante.
    """
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='clientes',
        verbose_name='Usuario'
    )
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    email = models.EmailField(max_length=50, verbose_name='Email')
    telefono = models.CharField(max_length=50, verbose_name='Teléfono')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['usuario', 'email']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'email'],
                name='unique_email_per_user'
            )
        ]

    def __str__(self):
        return self.nombre


class Mesa(models.Model):
    """
    Modelo de Mesa - Representa las mesas del restaurante.
    """
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mesas',
        verbose_name='Usuario'
    )
    numero_mesa = models.PositiveIntegerField(verbose_name='Número de Mesa')
    capacidad = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message='La capacidad mínima es 1 persona'),
            MaxValueValidator(20, message='La capacidad máxima es 20 personas')
        ],
        verbose_name='Capacidad'
    )
    activa = models.BooleanField(default=True, verbose_name='Activa')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado')

    class Meta:
        verbose_name = 'Mesa'
        verbose_name_plural = 'Mesas'
        ordering = ['numero_mesa']
        indexes = [
            models.Index(fields=['usuario', 'numero_mesa']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'numero_mesa'],
                name='unique_mesa_per_user'
            )
        ]

    def __str__(self):
        return f"Mesa {self.numero_mesa} - Capacidad {self.capacidad}"

    def clean(self):
        """
        Validación personalizada para Mesa.
        """
        super().clean()
        
        # Validar que el número de mesa sea positivo
        if self.numero_mesa and self.numero_mesa <= 0:
            raise ValidationError({
                'numero_mesa': 'El número de mesa debe ser mayor a 0.'
            })
        
        # Validar que la capacidad esté en el rango permitido
        if self.capacidad:
            if self.capacidad < 1:
                raise ValidationError({
                    'capacidad': 'La capacidad debe ser al menos 1 persona.'
                })
            if self.capacidad > 20:
                raise ValidationError({
                    'capacidad': 'La capacidad máxima es 20 personas.'
                })


class Reserva(models.Model):
    """
    Modelo de Reserva - Representa las reservas de mesas.
    """
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservas',
        verbose_name='Usuario'
    )
    fecha = models.DateField(verbose_name='Fecha')
    hora = models.TimeField(verbose_name='Hora')
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='reservas',
        verbose_name='Cliente'
    )
    mesa = models.ForeignKey(
        Mesa,
        on_delete=models.CASCADE,
        related_name='reservas',
        verbose_name='Mesa'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name='Estado'
    )
    notas = models.TextField(blank=True, null=True, verbose_name='Notas')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado')

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-fecha', '-hora']
        indexes = [
            models.Index(fields=['fecha', 'hora']),
            models.Index(fields=['mesa', 'fecha']),
            models.Index(fields=['estado']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['mesa', 'fecha', 'hora'],
                name='unique_reservation_per_mesa_datetime'
            )
        ]

    def __str__(self):
        return f"Reserva de {self.cliente} para la Mesa {self.mesa.numero_mesa} el {self.fecha} a las {self.hora}"

    @property
    def es_pasada(self):
        """
        Verifica si la reserva ya pasó.
        """
        from datetime import datetime, date
        fecha_hora_reserva = datetime.combine(self.fecha, self.hora)
        return fecha_hora_reserva < datetime.now()

    def clean(self):
        """
        Validación personalizada para Reserva.
        Verifica disponibilidad de mesa y horarios válidos.
        """
        super().clean()
        
        # Validar que la fecha no sea en el pasado
        if self.fecha and self.fecha < timezone.now().date():
            raise ValidationError({
                'fecha': 'No se pueden hacer reservas en fechas pasadas.'
            })
        
        # Validar horario de atención (12:00 - 23:00)
        if self.hora:
            hour = self.hora.hour
            if hour < 12 or hour >= 23:
                raise ValidationError({
                    'hora': 'El horario de atención es de 12:00 a 23:00.'
                })
            
            # Validar que las reservas sean cada 30 minutos
            if self.hora.minute not in [0, 30]:
                raise ValidationError({
                    'hora': 'Las reservas solo se aceptan cada 30 minutos (ejemplo: 12:00, 12:30).'
                })
        
        # Validar disponibilidad de mesa
        if self.mesa and self.fecha and self.hora:
            # Excluir la reserva actual si estamos editando
            reservas_existentes = Reserva.objects.filter(
                mesa=self.mesa,
                fecha=self.fecha,
                hora=self.hora
            ).exclude(estado='cancelada')
            
            if self.pk:  # Si estamos editando
                reservas_existentes = reservas_existentes.exclude(pk=self.pk)
            
            if reservas_existentes.exists():
                raise ValidationError({
                    'mesa': f'La mesa {self.mesa.numero_mesa} ya está reservada para el {self.fecha} a las {self.hora}.'
                })
        
        # Validar que el cliente y la mesa pertenezcan al mismo usuario
        if self.cliente and self.mesa:
            if self.cliente.usuario != self.mesa.usuario:
                raise ValidationError({
                    'mesa': 'La mesa y el cliente deben pertenecer al mismo usuario.'
                })
