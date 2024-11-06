from django.urls import path
from .views import (
    # Vistas de la API
    ClienteListCreateView, ClienteRetrieveUpdateDestroyView,
    MesaListCreateView, MesaRetrieveUpdateDestroyView,
    ReservaListCreateView, ReservaRetrieveUpdateDestroyView,
    # Vistas CRUD para los templates HTML
    cliente_list, cliente_create, cliente_update, cliente_delete,
    mesa_list, mesa_create, mesa_update, mesa_delete,
    reserva_list, reserva_create, reserva_update, reserva_delete,
)

urlpatterns = [
    # Rutas para la API de Cliente
    path('api/clientes/', ClienteListCreateView.as_view(), name='cliente-list-create'),
    path('api/clientes/<int:pk>/', ClienteRetrieveUpdateDestroyView.as_view(), name='cliente-retrieve-update-destroy'),

    # Rutas para la API de Mesa
    path('api/mesas/', MesaListCreateView.as_view(), name='mesa-list-create'),
    path('api/mesas/<int:pk>/', MesaRetrieveUpdateDestroyView.as_view(), name='mesa-retrieve-update-destroy'),

    # Rutas para la API de Reserva
    path('api/reservas/', ReservaListCreateView.as_view(), name='reserva-list-create'),
    path('api/reservas/<int:pk>/', ReservaRetrieveUpdateDestroyView.as_view(), name='reserva-retrieve-update-destroy'),

    # Rutas para los templates HTML de Cliente
    path('clientes/', cliente_list, name='cliente_list'),
    path('clientes/new/', cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/edit/', cliente_update, name='cliente_update'),
    path('clientes/<int:pk>/delete/', cliente_delete, name='cliente_delete'),

    # Rutas para los templates HTML de Mesa
    path('mesas/', mesa_list, name='mesa_list'),
    path('mesas/new/', mesa_create, name='mesa_create'),
    path('mesas/<int:pk>/edit/', mesa_update, name='mesa_update'),
    path('mesas/<int:pk>/delete/', mesa_delete, name='mesa_delete'),

    # Rutas para los templates HTML de Reserva
    path('reservas/', reserva_list, name='reserva_list'),
    path('reservas/new/', reserva_create, name='reserva_create'),
    path('reservas/<int:pk>/edit/', reserva_update, name='reserva_update'),
    path('reservas/<int:pk>/delete/', reserva_delete, name='reserva_delete'),
]
