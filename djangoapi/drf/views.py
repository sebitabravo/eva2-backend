# views.py
from django.shortcuts import render

# Vista para la raíz
def home(request):
    return render(request, 'home.html')
