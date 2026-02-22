from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Alumno, Docente


@receiver(post_save, sender=Alumno)
def crear_usuario_al_crear_alumno(sender, instance: Alumno, created: bool, **kwargs):
    if not created:
        return

    user_model = get_user_model()
    user, user_created = user_model.objects.get_or_create(
        dni=instance.dni,
        defaults={
            'email': instance.email,
            'username': instance.dni,
            'rol': user_model.Rol.ALUMNO,
            'alumno': instance,
            'debe_cambiar_password': True,
        },
    )

    if user_created:
        user.set_password(instance.dni)
        user.save(update_fields=['password'])
        return

    updates = []
    if user.alumno_id != instance.id:
        user.alumno = instance
        updates.append('alumno')
    if user.rol != user_model.Rol.ALUMNO:
        user.rol = user_model.Rol.ALUMNO
        updates.append('rol')
    if user.email != instance.email:
        user.email = instance.email
        updates.append('email')
    if not user.debe_cambiar_password:
        user.debe_cambiar_password = True
        updates.append('debe_cambiar_password')

    user.set_password(instance.dni)
    updates.append('password')

    if updates:
        user.save(update_fields=updates)


@receiver(post_save, sender=Docente)
def crear_usuario_al_crear_docente(sender, instance: Docente, created: bool, **kwargs):
    if not created:
        return

    user_model = get_user_model()
    user, user_created = user_model.objects.get_or_create(
        dni=instance.dni,
        defaults={
            'email': instance.email,
            'username': instance.dni,
            'rol': user_model.Rol.DOCENTE,
            'docente': instance,
            'debe_cambiar_password': True,
        },
    )

    if user_created:
        user.set_password(instance.dni)
        user.save(update_fields=['password'])
        return

    updates = []
    if user.docente_id != instance.id:
        user.docente = instance
        updates.append('docente')
    if user.rol != user_model.Rol.DOCENTE:
        user.rol = user_model.Rol.DOCENTE
        updates.append('rol')
    if user.email != instance.email:
        user.email = instance.email
        updates.append('email')
    if not user.debe_cambiar_password:
        user.debe_cambiar_password = True
        updates.append('debe_cambiar_password')

    user.set_password(instance.dni)
    updates.append('password')

    if updates:
        user.save(update_fields=updates)
