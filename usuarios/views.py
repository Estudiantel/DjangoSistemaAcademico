from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import Alumno, Carrera, Materia, Usuario


class RolRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    allowed_roles: tuple[str, ...] = ()

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return getattr(user, 'rol', None) in self.allowed_roles

    def handle_no_permission(self):
        messages.error(self.request, 'No tenés permisos para acceder a esta sección.')
        if self.request.user.is_authenticated:
            return redirect('usuarios:carrera-list')
        return super().handle_no_permission()


class SuccessMessageMixin:
    success_message = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response


class DeleteSuccessMessageMixin:
    success_message = ''

    def form_valid(self, form):
        if self.success_message:
            messages.success(self.request, self.success_message)
        return super().form_valid(form)


class CarreraListView(RolRequiredMixin, ListView):
    model = Carrera
    template_name = 'usuarios/carrera_list.html'
    context_object_name = 'carreras'
    allowed_roles = (Usuario.Rol.ADMINISTRADOR, Usuario.Rol.INVITADO, Usuario.Rol.ALUMNO)


class CarreraCreateView(RolRequiredMixin, SuccessMessageMixin, CreateView):
    model = Carrera
    fields = ['nombre', 'duracion']
    template_name = 'usuarios/form.html'
    success_url = reverse_lazy('usuarios:carrera-list')
    success_message = 'Carrera creada correctamente.'
    allowed_roles = (Usuario.Rol.ADMINISTRADOR,)


class CarreraUpdateView(RolRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Carrera
    fields = ['nombre', 'duracion']
    template_name = 'usuarios/form.html'
    success_url = reverse_lazy('usuarios:carrera-list')
    success_message = 'Carrera actualizada correctamente.'
    allowed_roles = (Usuario.Rol.ADMINISTRADOR,)


class CarreraDeleteView(RolRequiredMixin, DeleteSuccessMessageMixin, DeleteView):
    model = Carrera
    template_name = 'usuarios/confirm_delete.html'
    success_url = reverse_lazy('usuarios:carrera-list')
    success_message = 'Carrera eliminada correctamente.'
    allowed_roles = (Usuario.Rol.ADMINISTRADOR,)


class MateriaListView(RolRequiredMixin, ListView):
    model = Materia
    template_name = 'usuarios/materia_list.html'
    context_object_name = 'materias'
    allowed_roles = (Usuario.Rol.ADMINISTRADOR, Usuario.Rol.INVITADO, Usuario.Rol.ALUMNO)


class MateriaCreateView(RolRequiredMixin, SuccessMessageMixin, CreateView):
    model = Materia
    fields = ['nombre', 'carrera', 'cupo_maximo']
    template_name = 'usuarios/form.html'
    success_url = reverse_lazy('usuarios:materia-list')
    success_message = 'Materia creada correctamente.'
    allowed_roles = (Usuario.Rol.ADMINISTRADOR,)


class MateriaUpdateView(RolRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Materia
    fields = ['nombre', 'carrera', 'cupo_maximo']
    template_name = 'usuarios/form.html'
    success_url = reverse_lazy('usuarios:materia-list')
    success_message = 'Materia actualizada correctamente.'
    allowed_roles = (Usuario.Rol.ADMINISTRADOR,)


class MateriaDeleteView(RolRequiredMixin, DeleteSuccessMessageMixin, DeleteView):
    model = Materia
    template_name = 'usuarios/confirm_delete.html'
    success_url = reverse_lazy('usuarios:materia-list')
    success_message = 'Materia eliminada correctamente.'
    allowed_roles = (Usuario.Rol.ADMINISTRADOR,)


class AlumnoListView(RolRequiredMixin, ListView):
    model = Alumno
    template_name = 'usuarios/alumno_list.html'
    context_object_name = 'alumnos'
    allowed_roles = (Usuario.Rol.ADMINISTRADOR,)


class AlumnoCreateView(RolRequiredMixin, SuccessMessageMixin, CreateView):
    model = Alumno
    fields = ['nombre', 'apellido', 'dni', 'email', 'legajo']
    template_name = 'usuarios/form.html'
    success_url = reverse_lazy('usuarios:alumno-list')
    success_message = 'Alumno creado correctamente.'
    allowed_roles = (Usuario.Rol.ADMINISTRADOR,)


class AlumnoUpdateView(RolRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Alumno
    fields = ['nombre', 'apellido', 'dni', 'email', 'legajo']
    template_name = 'usuarios/form.html'
    success_url = reverse_lazy('usuarios:alumno-list')
    success_message = 'Alumno actualizado correctamente.'
    allowed_roles = (Usuario.Rol.ADMINISTRADOR,)


class AlumnoDeleteView(RolRequiredMixin, DeleteSuccessMessageMixin, DeleteView):
    model = Alumno
    template_name = 'usuarios/confirm_delete.html'
    success_url = reverse_lazy('usuarios:alumno-list')
    success_message = 'Alumno eliminado correctamente.'
    allowed_roles = (Usuario.Rol.ADMINISTRADOR,)
