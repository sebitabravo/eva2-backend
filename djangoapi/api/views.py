# Importaciones para la API REST
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import timedelta

from .models import Cliente, Mesa, Reserva
from .serializers import ClienteSerializer, MesaSerializer, ReservaSerializer
from .permissions import IsAdminOrReadOnly
from .throttling import WriteThrottle, ReadThrottle, StatsThrottle

class ClienteViewSet(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    permission_classes = [IsAdminOrReadOnly]

    @method_decorator(cache_page(60))
    @method_decorator(vary_on_headers("Authorization"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return Cliente.objects.all().order_by('-id')

    def get_throttles(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [WriteThrottle()]
        return [ReadThrottle()]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=True, methods=['get'], url_path='estadisticas', throttle_classes=[StatsThrottle])
    def estadisticas(self, request, pk=None):
        """
        Endpoint de estadísticas por cliente.
        Retorna información agregada sobre las reservas del cliente.
        """
        cliente = self.get_object()
        
        # Total de reservas del cliente
        total_reservas = cliente.reservas.count()
        
        # Reservas por estado
        reservas_pendientes = cliente.reservas.filter(estado='pendiente').count()
        reservas_confirmadas = cliente.reservas.filter(estado='confirmada').count()
        reservas_canceladas = cliente.reservas.filter(estado='cancelada').count()
        reservas_completadas = cliente.reservas.filter(estado='completada').count()
        
        # Reservas futuras vs pasadas
        hoy = timezone.now().date()
        reservas_futuras = cliente.reservas.filter(fecha__gte=hoy).count()
        reservas_pasadas = cliente.reservas.filter(fecha__lt=hoy).count()
        
        # Última reserva
        ultima_reserva = cliente.reservas.order_by('-fecha', '-hora').first()
        ultima_reserva_info = None
        if ultima_reserva:
            ultima_reserva_info = {
                'fecha': ultima_reserva.fecha,
                'hora': ultima_reserva.hora,
                'mesa': ultima_reserva.mesa.numero_mesa,
                'estado': ultima_reserva.estado
            }
        
        # Próxima reserva
        proxima_reserva = cliente.reservas.filter(
            fecha__gte=hoy
        ).order_by('fecha', 'hora').first()
        proxima_reserva_info = None
        if proxima_reserva:
            proxima_reserva_info = {
                'fecha': proxima_reserva.fecha,
                'hora': proxima_reserva.hora,
                'mesa': proxima_reserva.mesa.numero_mesa,
                'estado': proxima_reserva.estado
            }
        
        return Response({
            'cliente': {
                'id': cliente.id,
                'nombre': cliente.nombre,
                'email': cliente.email
            },
            'estadisticas': {
                'total_reservas': total_reservas,
                'por_estado': {
                    'pendientes': reservas_pendientes,
                    'confirmadas': reservas_confirmadas,
                    'canceladas': reservas_canceladas,
                    'completadas': reservas_completadas
                },
                'temporales': {
                    'futuras': reservas_futuras,
                    'pasadas': reservas_pasadas
                },
                'ultima_reserva': ultima_reserva_info,
                'proxima_reserva': proxima_reserva_info
            }
        })


class MesaViewSet(viewsets.ModelViewSet):
    serializer_class = MesaSerializer
    permission_classes = [IsAdminOrReadOnly]

    @method_decorator(cache_page(60))
    @method_decorator(vary_on_headers("Authorization"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return Mesa.objects.all().order_by('numero_mesa')

    def get_throttles(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [WriteThrottle()]
        return [ReadThrottle()]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=True, methods=['get'], url_path='estadisticas', throttle_classes=[StatsThrottle])
    def estadisticas(self, request, pk=None):
        """
        Endpoint de estadísticas por mesa.
        Retorna información agregada sobre las reservas de la mesa.
        """
        mesa = self.get_object()
        
        # Total de reservas de la mesa
        total_reservas = mesa.reservas.count()
        
        # Reservas por estado
        reservas_pendientes = mesa.reservas.filter(estado='pendiente').count()
        reservas_confirmadas = mesa.reservas.filter(estado='confirmada').count()
        reservas_canceladas = mesa.reservas.filter(estado='cancelada').count()
        reservas_completadas = mesa.reservas.filter(estado='completada').count()
        
        # Tasa de ocupación (últimos 30 días)
        hace_30_dias = timezone.now().date() - timedelta(days=30)
        reservas_ultimo_mes = mesa.reservas.filter(
            fecha__gte=hace_30_dias,
            estado__in=['confirmada', 'completada']
        ).count()
        
        # Reservas futuras
        hoy = timezone.now().date()
        reservas_futuras = mesa.reservas.filter(fecha__gte=hoy).count()
        
        # Última reserva
        ultima_reserva = mesa.reservas.order_by('-fecha', '-hora').first()
        ultima_reserva_info = None
        if ultima_reserva:
            ultima_reserva_info = {
                'fecha': ultima_reserva.fecha,
                'hora': ultima_reserva.hora,
                'cliente': ultima_reserva.cliente.nombre,
                'estado': ultima_reserva.estado
            }
        
        # Próxima reserva
        proxima_reserva = mesa.reservas.filter(
            fecha__gte=hoy
        ).order_by('fecha', 'hora').first()
        proxima_reserva_info = None
        if proxima_reserva:
            proxima_reserva_info = {
                'fecha': proxima_reserva.fecha,
                'hora': proxima_reserva.hora,
                'cliente': proxima_reserva.cliente.nombre,
                'estado': proxima_reserva.estado
            }
        
        # Horarios más populares
        horarios_populares = mesa.reservas.values('hora').annotate(
            total=Count('id')
        ).order_by('-total')[:5]
        
        return Response({
            'mesa': {
                'id': mesa.id,
                'numero_mesa': mesa.numero_mesa,
                'capacidad': mesa.capacidad,
                'activa': mesa.activa
            },
            'estadisticas': {
                'total_reservas': total_reservas,
                'por_estado': {
                    'pendientes': reservas_pendientes,
                    'confirmadas': reservas_confirmadas,
                    'canceladas': reservas_canceladas,
                    'completadas': reservas_completadas
                },
                'ocupacion': {
                    'ultimo_mes': reservas_ultimo_mes,
                    'futuras': reservas_futuras
                },
                'horarios_populares': list(horarios_populares),
                'ultima_reserva': ultima_reserva_info,
                'proxima_reserva': proxima_reserva_info
            }
        })


class ReservaViewSet(viewsets.ModelViewSet):
    serializer_class = ReservaSerializer
    permission_classes = [IsAdminOrReadOnly]

    @method_decorator(cache_page(60))
    @method_decorator(vary_on_headers("Authorization"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return Reserva.objects.all().select_related('cliente', 'mesa').order_by('-fecha', '-hora')

    def get_throttles(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [WriteThrottle()]
        return [ReadThrottle()]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=False, methods=['get'], url_path='estadisticas', throttle_classes=[StatsThrottle])
    def estadisticas(self, request):
        """
        Endpoint de estadísticas generales del sistema de reservas.
        Retorna métricas agregadas de todas las reservas.
        """
        # Total de reservas
        total_reservas = Reserva.objects.count()
        
        # Reservas por estado
        reservas_por_estado = {
            'pendientes': Reserva.objects.filter(estado='pendiente').count(),
            'confirmadas': Reserva.objects.filter(estado='confirmada').count(),
            'canceladas': Reserva.objects.filter(estado='cancelada').count(),
            'completadas': Reserva.objects.filter(estado='completada').count()
        }
        
        # Reservas por periodo
        hoy = timezone.now().date()
        hace_7_dias = hoy - timedelta(days=7)
        hace_30_dias = hoy - timedelta(days=30)
        
        reservas_hoy = Reserva.objects.filter(fecha=hoy).count()
        reservas_semana = Reserva.objects.filter(fecha__gte=hace_7_dias).count()
        reservas_mes = Reserva.objects.filter(fecha__gte=hace_30_dias).count()
        
        # Reservas futuras vs pasadas
        reservas_futuras = Reserva.objects.filter(fecha__gte=hoy).count()
        reservas_pasadas = Reserva.objects.filter(fecha__lt=hoy).count()
        
        # Mesas más reservadas
        mesas_populares = Reserva.objects.values(
            'mesa__numero_mesa', 'mesa__capacidad'
        ).annotate(
            total_reservas=Count('id')
        ).order_by('-total_reservas')[:5]
        
        # Clientes más frecuentes
        clientes_frecuentes = Reserva.objects.values(
            'cliente__nombre', 'cliente__email'
        ).annotate(
            total_reservas=Count('id')
        ).order_by('-total_reservas')[:5]
        
        # Horarios más populares
        horarios_populares = Reserva.objects.values('hora').annotate(
            total=Count('id')
        ).order_by('-total')[:5]
        
        # Días de la semana más populares (compatible con SQLite y PostgreSQL)
        from django.db import connection
        
        reservas_ultimas = Reserva.objects.filter(fecha__gte=hace_30_dias)
        dias_semana = {}
        dias_nombres = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
        
        for reserva in reservas_ultimas:
            dia_num = reserva.fecha.weekday()  # 0=Lunes, 6=Domingo
            # Ajustar para que 0=Domingo como strftime
            dia_num = (dia_num + 1) % 7
            dia_nombre = dias_nombres[dia_num]
            dias_semana[dia_nombre] = dias_semana.get(dia_nombre, 0) + 1
        
        reservas_por_dia = [{'dia': k, 'total': v} for k, v in sorted(dias_semana.items(), key=lambda x: x[1], reverse=True)]
        
        # Tasa de cancelación
        if total_reservas > 0:
            tasa_cancelacion = (reservas_por_estado['canceladas'] / total_reservas) * 100
        else:
            tasa_cancelacion = 0
        
        # Promedio de reservas por día (últimos 30 días)
        if reservas_mes > 0:
            promedio_reservas_dia = reservas_mes / 30
        else:
            promedio_reservas_dia = 0
        
        return Response({
            'resumen_general': {
                'total_reservas': total_reservas,
                'reservas_hoy': reservas_hoy,
                'reservas_esta_semana': reservas_semana,
                'reservas_este_mes': reservas_mes
            },
            'distribucion_temporal': {
                'futuras': reservas_futuras,
                'pasadas': reservas_pasadas
            },
            'por_estado': reservas_por_estado,
            'metricas': {
                'tasa_cancelacion': round(tasa_cancelacion, 2),
                'promedio_reservas_por_dia': round(promedio_reservas_dia, 2)
            },
            'top_5': {
                'mesas_mas_reservadas': list(mesas_populares),
                'clientes_mas_frecuentes': list(clientes_frecuentes),
                'horarios_mas_populares': list(horarios_populares)
            },
            'tendencias': {
                'reservas_por_dia_semana': reservas_por_dia
            }
        })
