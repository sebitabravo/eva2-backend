from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Cliente, Mesa, Reserva
from datetime import date, time

class ReservaModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.cliente = Cliente.objects.create(
            usuario=self.user,
            nombre='Test Cliente',
            email='test@cliente.com',
            telefono='123456789'
        )
        self.mesa = Mesa.objects.create(
            usuario=self.user,
            numero_mesa=1,
            capacidad=4
        )

    def test_reserva_creation(self):
        reserva = Reserva.objects.create(
            usuario=self.user,
            cliente=self.cliente,
            mesa=self.mesa,
            fecha=date.today(),
            hora=time(20, 0)
        )
        self.assertEqual(reserva.cliente.nombre, 'Test Cliente')
        self.assertEqual(reserva.mesa.numero_mesa, 1)
        self.assertEqual(reserva.usuario.username, 'testuser')

class MesaModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_mesa_creation(self):
        mesa = Mesa.objects.create(
            usuario=self.user,
            numero_mesa=1,
            capacidad=4
        )
        self.assertEqual(mesa.numero_mesa, 1)
        self.assertEqual(mesa.capacidad, 4)
        self.assertEqual(mesa.usuario.username, 'testuser')

class ClienteModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_cliente_creation(self):
        cliente = Cliente.objects.create(
            usuario=self.user,
            nombre='Test Cliente',
            email='test@cliente.com',
            telefono='123456789'
        )
        self.assertEqual(cliente.nombre, 'Test Cliente')
        self.assertEqual(cliente.usuario.username, 'testuser')
