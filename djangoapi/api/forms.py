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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ReservaForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['cliente'].queryset = cliente.objects.filter(usuario=user)
            self.fields['mesa'].queryset = mesa.objects.filter(usuario=user)
