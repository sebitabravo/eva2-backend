from django.contrib import admin
from .models import Cliente, Mesa, Reserva

# Register your models here.

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'telefono', 'usuario', 'created_at']
    search_fields = ['nombre', 'email', 'telefono']
    list_filter = ['created_at', 'usuario']
    fieldsets = (
        (None, {
            'fields': ('usuario', 'nombre', 'email', 'telefono')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        })
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ['numero_mesa', 'capacidad', 'activa', 'usuario', 'created_at']
    search_fields = ['numero_mesa']
    list_filter = ['capacidad', 'activa', 'usuario']
    fieldsets = (
        (None, {
            'fields': ('usuario', 'numero_mesa', 'capacidad', 'activa')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        })
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'hora', 'cliente', 'mesa', 'estado', 'usuario', 'created_at']
    search_fields = ['cliente__nombre', 'mesa__numero_mesa']
    list_filter = ['fecha', 'estado', 'usuario']
    date_hierarchy = 'fecha'
    raw_id_fields = ('cliente', 'mesa')
    fieldsets = (
        (None, {
            'fields': ('usuario', 'cliente', 'mesa', 'fecha', 'hora', 'estado')
        }),
        ('Información Adicional', {
            'fields': ('notas',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        })
    )
    readonly_fields = ('created_at', 'updated_at')
