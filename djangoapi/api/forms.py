from django import forms
from .models import cliente, mesa, reserva

class ClienteForm(forms.ModelForm):
    class Meta:
        model = cliente
        fields = ['nombre', 'email', 'telefono']

class MesaForm(forms.ModelForm):
    class Meta:
        model = mesa
        fields = ['numero_mesa', 'capacidad']

class ReservaForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # Selector de fecha
        label="Fecha de la reserva"
    )
    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),  # Selector de hora
        label="Hora de la reserva"
    )
    cliente = forms.ModelChoiceField(
        queryset=cliente.objects.all(),  # Muestra clientes disponibles
        label="Cliente"
    )
    mesa = forms.ModelChoiceField(
        queryset=mesa.objects.all(),  # Muestra mesas disponibles
        label="Mesa"
    )

    class Meta:
        model = reserva
        fields = ['fecha', 'hora', 'cliente', 'mesa']
