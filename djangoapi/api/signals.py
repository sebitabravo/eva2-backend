from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Cliente

@receiver(post_save, sender=User)
def create_cliente(sender, instance, created, **kwargs):
    if created:
        Cliente.objects.create(usuario=instance, nombre=instance.username, email=instance.email)