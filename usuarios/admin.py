from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Alumno, Carrera, Inscripcion, Materia, Usuario


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'dni', 'email', 'legajo')
    search_fields = ('apellido', 'nombre', 'dni', 'email', 'legajo')


@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'duracion')
    search_fields = ('nombre',)


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'carrera', 'cupo_maximo')
    search_fields = ('nombre', 'carrera__nombre')
    list_filter = ('carrera',)


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'materia', 'fecha_inscripcion')
    search_fields = ('alumno__apellido', 'alumno__nombre', 'materia__nombre')
    list_filter = ('materia__carrera', 'materia')


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    ordering = ('dni',)
    list_display = ('dni', 'email', 'rol', 'is_staff', 'debe_cambiar_password', 'alumno')
    search_fields = ('dni', 'email', 'username')

    fieldsets = UserAdmin.fieldsets + (
        (
            'Datos académicos',
            {'fields': ('dni', 'rol', 'debe_cambiar_password', 'alumno')},
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Datos académicos',
            {'fields': ('dni', 'email', 'rol', 'debe_cambiar_password', 'alumno')},
        ),
    )
