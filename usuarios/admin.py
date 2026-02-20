from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Alumno, Usuario


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'dni', 'email', 'legajo')
    search_fields = ('apellido', 'nombre', 'dni', 'email', 'legajo')


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
