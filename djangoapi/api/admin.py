from django.contrib import admin
from .models import cliente, mesa, reserva

# Register your models here.

@admin.register(cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'telefono']
    search_fields = ['nombre', 'email']
    list_filter = ['nombre']

@admin.register(mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ['numero_mesa', 'capacidad']
    search_fields = ['numero_mesa']
    list_filter = ['capacidad']

@admin.register(reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'hora']
    search_fields = ['cliente__nombre', 'mesa__numero_mesa']
    list_filter = ['fecha', 'hora']
    date_hierarchy = 'fecha'
