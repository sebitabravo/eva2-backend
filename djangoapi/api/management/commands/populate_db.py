"""
Management command para poblar la base de datos con datos de ejemplo
Uso: python manage.py populate_db
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from api.models import Cliente, Mesa, Reserva
import random


class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de ejemplo para desarrollo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Elimina todos los datos antes de poblar',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Eliminando datos existentes...'))
            Reserva.objects.all().delete()
            Mesa.objects.all().delete()
            Cliente.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ Datos eliminados'))

        # Verificar si ya existen datos
        if Cliente.objects.exists() or Mesa.objects.exists() or Reserva.objects.exists():
            self.stdout.write(self.style.WARNING(
                'La base de datos ya contiene datos. Use --clear para eliminarlos primero.'
            ))
            return

        self.stdout.write(self.style.MIGRATE_HEADING('Poblando base de datos...'))

        # Obtener o crear usuario de prueba
        try:
            user = User.objects.get(username='admin')
        except User.DoesNotExist:
            user = User.objects.create_superuser(
                username='admin',
                email='admin@reservas.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('✓ Usuario admin creado (usuario: admin, password: admin123)'))

        with transaction.atomic():
            # Crear clientes
            clientes_data = [
                {'nombre': 'Juan Pérez', 'email': 'juan.perez@email.com', 'telefono': '912345678'},
                {'nombre': 'María González', 'email': 'maria.gonzalez@email.com', 'telefono': '923456789'},
                {'nombre': 'Carlos Rodríguez', 'email': 'carlos.rodriguez@email.com', 'telefono': '934567890'},
                {'nombre': 'Ana Martínez', 'email': 'ana.martinez@email.com', 'telefono': '945678901'},
                {'nombre': 'Pedro Sánchez', 'email': 'pedro.sanchez@email.com', 'telefono': '956789012'},
                {'nombre': 'Laura Torres', 'email': 'laura.torres@email.com', 'telefono': '967890123'},
                {'nombre': 'Diego Ramírez', 'email': 'diego.ramirez@email.com', 'telefono': '978901234'},
                {'nombre': 'Carmen Flores', 'email': 'carmen.flores@email.com', 'telefono': '989012345'},
                {'nombre': 'Roberto Silva', 'email': 'roberto.silva@email.com', 'telefono': '990123456'},
                {'nombre': 'Patricia Díaz', 'email': 'patricia.diaz@email.com', 'telefono': '901234567'},
            ]

            clientes_list = []
            for data in clientes_data:
                c = Cliente.objects.create(usuario=user, **data)
                clientes_list.append(c)

            self.stdout.write(self.style.SUCCESS(f'✓ {len(clientes_list)} clientes creados'))

            # Crear mesas
            mesas_data = [
                {'numero_mesa': 1, 'capacidad': 2},
                {'numero_mesa': 2, 'capacidad': 2},
                {'numero_mesa': 3, 'capacidad': 4},
                {'numero_mesa': 4, 'capacidad': 4},
                {'numero_mesa': 5, 'capacidad': 4},
                {'numero_mesa': 6, 'capacidad': 6},
                {'numero_mesa': 7, 'capacidad': 6},
                {'numero_mesa': 8, 'capacidad': 8},
                {'numero_mesa': 9, 'capacidad': 8},
                {'numero_mesa': 10, 'capacidad': 10},
            ]

            mesas_list = []
            for data in mesas_data:
                m = Mesa.objects.create(usuario=user, **data)
                mesas_list.append(m)

            self.stdout.write(self.style.SUCCESS(f'✓ {len(mesas_list)} mesas creadas'))

            # Crear reservas
            reservas_count = 0
            hoy = timezone.now().date()
            horas_disponibles = ['12:00', '12:30', '13:00', '13:30', '14:00', '14:30',
                                '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30']

            # Generar reservas para los próximos 7 días
            for dia_offset in range(7):
                fecha = hoy + timedelta(days=dia_offset)

                # Crear entre 5-10 reservas por día
                num_reservas = random.randint(5, 10)

                # Mezclar mesas y horas para variedad
                mesas_disponibles = mesas_list.copy()
                random.shuffle(mesas_disponibles)

                for i in range(min(num_reservas, len(mesas_disponibles))):
                    mesa_obj = mesas_disponibles[i]
                    cliente_obj = random.choice(clientes_list)
                    hora_str = random.choice(horas_disponibles)

                    # Convertir hora string a time object
                    hora_parts = hora_str.split(':')
                    hora_obj = timezone.datetime.strptime(hora_str, '%H:%M').time()

                    # Verificar que no exista conflicto
                    if not Reserva.objects.filter(
                        fecha=fecha,
                        hora=hora_obj,
                        mesa=mesa_obj
                    ).exists():
                        Reserva.objects.create(
                            usuario=user,
                            fecha=fecha,
                            hora=hora_obj,
                            cliente=cliente_obj,
                            mesa=mesa_obj
                        )
                        reservas_count += 1

            self.stdout.write(self.style.SUCCESS(f'✓ {reservas_count} reservas creadas'))

        self.stdout.write(self.style.SUCCESS(
            '\n' + '='*60 +
            '\n✓ Base de datos poblada exitosamente!' +
            '\n' + '='*60 +
            '\n\nResumen:' +
            f'\n  - Clientes: {len(clientes_list)}' +
            f'\n  - Mesas: {len(mesas_list)}' +
            f'\n  - Reservas: {reservas_count}' +
            '\n\nCredenciales de acceso:' +
            '\n  Usuario: admin' +
            '\n  Password: admin123' +
            '\n'
        ))
