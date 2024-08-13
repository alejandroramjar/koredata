from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Usuario

@receiver(post_save, sender=Usuario)
def registrar_actividad(sender, instance, created, **kwargs):
    if created:
        print(f'Nuevo usuario registrado: {instance.username}')
    else:
        print(f'Usuario actualizado: {instance.username}')
