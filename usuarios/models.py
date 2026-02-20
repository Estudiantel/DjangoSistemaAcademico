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
    carrera = models.ForeignKey(
        'Carrera',
        on_delete=models.PROTECT,
        related_name='alumnos',
        null=True,
        blank=True,
    )


class Carrera(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    duracion = models.PositiveIntegerField(help_text='Duración en años.')

    def __str__(self) -> str:
        return self.nombre


class Materia(models.Model):
    nombre = models.CharField(max_length=150)
    carrera = models.ForeignKey(Carrera, on_delete=models.PROTECT, related_name='materias')
    cupo_maximo = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nombre', 'carrera'],
                name='unique_materia_nombre_por_carrera',
            )
        ]

    def __str__(self) -> str:
        return f'{self.nombre} ({self.carrera.nombre})'

    @property
    def cupo_disponible(self) -> int:
        return max(self.cupo_maximo - self.inscripciones.count(), 0)


class Inscripcion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.PROTECT, related_name='inscripciones')
    materia = models.ForeignKey(Materia, on_delete=models.PROTECT, related_name='inscripciones')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['alumno', 'materia'],
                name='unique_inscripcion_alumno_materia',
            )
        ]

    def __str__(self) -> str:
        return f'{self.alumno} - {self.materia}'


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
