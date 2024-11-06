# Importaciones para las vistas basadas en funciones (HTML templates)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import cliente, mesa, reserva
from .forms import ClienteForm, MesaForm, ReservaForm  # Asegúrate de tener estos formularios creados en forms.py

# Importaciones para las vistas basadas en clases (API REST)
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializer import ClienteSerializer, MesaSerializer, ReservaSerializer


# ==============================
# Sección 1: Vistas basadas en funciones para CRUD en HTML templates
# ==============================

# Cliente CRUD Views
@login_required
def cliente_list(request):
    clientes = cliente.objects.filter(usuario=request.user)
    return render(request, 'clientes/list.html', {'clientes': clientes})

@login_required
def cliente_create(request):
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        cliente_instance = form.save(commit=False)
        cliente_instance.usuario = request.user  # Asigna el usuario autenticado
        cliente_instance.save()
        return redirect('cliente_list')
    return render(request, 'clientes/form.html', {'form': form})

@login_required
def cliente_update(request, pk):
    cliente_instance = get_object_or_404(cliente, pk=pk, usuario=request.user)
    form = ClienteForm(request.POST or None, instance=cliente_instance)
    if form.is_valid():
        form.save()
        return redirect('cliente_list')
    return render(request, 'clientes/form.html', {'form': form})

@login_required
def cliente_delete(request, pk):
    cliente_instance = get_object_or_404(cliente, pk=pk, usuario=request.user)
    if request.method == 'POST':
        cliente_instance.delete()
        return redirect('cliente_list')
    return render(request, 'clientes/confirm_delete.html', {'object': cliente_instance})


# Mesa CRUD Views
@login_required
def mesa_list(request):
    mesas = mesa.objects.filter(usuario=request.user)
    return render(request, 'mesas/list.html', {'mesas': mesas})

@login_required
def mesa_create(request):
    form = MesaForm(request.POST or None)
    if form.is_valid():
        mesa_instance = form.save(commit=False)
        mesa_instance.usuario = request.user
        mesa_instance.save()
        return redirect('mesa_list')
    return render(request, 'mesas/form.html', {'form': form})

@login_required
def mesa_update(request, pk):
    mesa_instance = get_object_or_404(mesa, pk=pk, usuario=request.user)
    form = MesaForm(request.POST or None, instance=mesa_instance)
    if form.is_valid():
        form.save()
        return redirect('mesa_list')
    return render(request, 'mesas/form.html', {'form': form})

@login_required
def mesa_delete(request, pk):
    mesa_instance = get_object_or_404(mesa, pk=pk, usuario=request.user)
    if request.method == 'POST':
        mesa_instance.delete()
        return redirect('mesa_list')
    return render(request, 'mesas/confirm_delete.html', {'object': mesa_instance})


# Reserva CRUD Views
@login_required
def reserva_list(request):
    reservas = reserva.objects.filter(usuario=request.user)
    return render(request, 'reservas/list.html', {'reservas': reservas})

@login_required
def reserva_create(request):
    form = ReservaForm(request.POST or None)
    if form.is_valid():
        reserva_instance = form.save(commit=False)
        reserva_instance.usuario = request.user
        reserva_instance.save()
        return redirect('reserva_list')
    return render(request, 'reservas/form.html', {'form': form})

@login_required
def reserva_update(request, pk):
    reserva_instance = get_object_or_404(reserva, pk=pk, usuario=request.user)
    form = ReservaForm(request.POST or None, instance=reserva_instance)
    if form.is_valid():
        form.save()
        return redirect('reserva_list')
    return render(request, 'reservas/form.html', {'form': form})

@login_required
def reserva_delete(request, pk):
    reserva_instance = get_object_or_404(reserva, pk=pk, usuario=request.user)
    if request.method == 'POST':
        reserva_instance.delete()
        return redirect('reserva_list')
    return render(request, 'reservas/confirm_delete.html', {'object': reserva_instance})


# ==============================
# Sección 2: Vistas basadas en clases para API REST
# ==============================

# Vistas de la API para Cliente
class ClienteListCreateView(generics.ListCreateAPIView):
    queryset = cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

class ClienteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

# Vistas de la API para Mesa
class MesaListCreateView(generics.ListCreateAPIView):
    queryset = mesa.objects.all()
    serializer_class = MesaSerializer
    permission_classes = [IsAuthenticated]

class MesaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = mesa.objects.all()
    serializer_class = MesaSerializer
    permission_classes = [IsAuthenticated]

# Vistas de la API para Reserva
class ReservaListCreateView(generics.ListCreateAPIView):
    queryset = reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated]

class ReservaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated]
