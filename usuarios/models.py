from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, dni: str, email: str, password: str | None, **extra_fields):
        if not dni:
            raise ValueError('El DNI es obligatorio.')
        if not email:
            raise ValueError('El email es obligatorio.')

        email = self.normalize_email(email)
        user = self.model(dni=dni, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, dni: str, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(dni, email, password, **extra_fields)

    def create_superuser(self, dni: str, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self._create_user(dni, email, password, **extra_fields)


class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f'{self.apellido}, {self.nombre}'


class Alumno(Persona):
    legajo = models.CharField(max_length=30, unique=True)


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador'
        ALUMNO = 'ALUMNO', 'Alumno'
        INVITADO = 'INVITADO', 'Invitado'

    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    dni = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, choices=Rol.choices)
    debe_cambiar_password = models.BooleanField(default=True)
    alumno = models.OneToOneField(
        Alumno,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuario',
        help_text='Vincular cuando el usuario tenga rol Alumno.',
    )

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['email']

    objects = UsuarioManager()

    def save(self, *args, **kwargs):
        if self.rol != self.Rol.ALUMNO:
            self.alumno = None
        super().save(*args, **kwargs)
