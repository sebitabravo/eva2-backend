"""
Custom throttling classes for differentiated rate limiting
"""

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class ReadThrottle(AnonRateThrottle):
    """
    Throttling para operaciones de lectura (GET).
    Más permisivo que el throttling de escritura.
    """
    scope = 'read'


class WriteThrottle(UserRateThrottle):
    """
    Throttling restrictivo para operaciones de escritura (POST, PUT, PATCH, DELETE).
    Requiere autenticación y limita operaciones de modificación.
    """
    scope = 'write'


class BurstThrottle(AnonRateThrottle):
    """
    Throttling de ráfaga para prevenir picos de tráfico.
    Se aplica tanto a usuarios autenticados como anónimos.
    """
    scope = 'burst'


class StatsThrottle(UserRateThrottle):
    """
    Throttling específico para endpoints de estadísticas.
    Más restrictivo ya que son operaciones costosas con agregaciones complejas.
    """
    scope = 'stats'
