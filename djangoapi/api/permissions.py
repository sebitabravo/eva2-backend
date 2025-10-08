"""
Custom permissions for public read-only API access
"""

from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permite acceso de lectura (GET, HEAD, OPTIONS) a cualquier usuario.
    Solo usuarios administradores pueden realizar operaciones de escritura
    (POST, PUT, PATCH, DELETE).

    Uso:
        permission_classes = [IsAdminOrReadOnly]
    """

    def has_permission(self, request, view):
        # Métodos seguros (GET, HEAD, OPTIONS) están permitidos para todos
        if request.method in permissions.SAFE_METHODS:
            return True

        # Operaciones de escritura solo para staff/admin
        return request.user and request.user.is_staff
