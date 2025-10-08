from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, MesaViewSet, ReservaViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'mesas', MesaViewSet, basename='mesa')
router.register(r'reservas', ReservaViewSet, basename='reserva')

urlpatterns = [
    path('v1/', include(router.urls)),
]
