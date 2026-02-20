from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import AlumnoForm, CarreraForm, MateriaForm
from .models import Alumno, Carrera, Inscripcion, Materia, Usuario
from .services import inscribir_alumno


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


class PrimerLoginPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.debe_cambiar_password:
            self.request.user.debe_cambiar_password = False
            self.request.user.save(update_fields=['debe_cambiar_password'])
        messages.success(self.request, 'Contraseña actualizada correctamente.')
        return response


class CarreraListView(RolRequiredMixin, ListView):
    model = Carrera
    template_name = 'usuarios/carrera_list.html'
    context_object_name = 'carreras'
    allowed_roles = (Usuario.Rol.ADMINISTRADOR, Usuario.Rol.INVITADO, Usuario.Rol.ALUMNO)


class CarreraCreateView(RolRequiredMixin, SuccessMessageMixin, CreateView):
    model = Carrera
    form_class = CarreraForm
    template_name = 'usuarios/form.html'
    success_url = reverse_lazy('usuarios:carrera-list')
    success_message = 'Carrera creada correctamente.'
    extra_context = {'titulo': 'Crear Carrera'}
    allowed_roles = (Usuario.Rol.ADMINISTRADOR,)


class CarreraUpdateView(RolRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Carrera
    form_class = CarreraForm
    template_name = 'usuarios/form.html'
    success_url = reverse_lazy('usuarios:carrera-list')
    success_message = 'Carrera actualizada correctamente.'
    extra_context = {'titulo': 'Editar Carrera'}
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

    def get_queryset(self):
        queryset = Materia.objects.select_related('carrera')
        user = self.request.user
        if user.is_superuser or user.rol == Usuario.Rol.ADMINISTRADOR:
            carrera_id = self.request.GET.get('carrera')
            if carrera_id:
                queryset = queryset.filter(carrera_id=carrera_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_superuser or user.rol == Usuario.Rol.ADMINISTRADOR:
            context['carreras'] = Carrera.objects.order_by('nombre')
            context['carrera_seleccionada'] = self.request.GET.get('carrera', '')
        return context


class MateriaCreateView(RolRequiredMixin, SuccessMessageMixin, CreateView):
    model = Materia
    form_class = MateriaForm
    template_name = 'usuarios/form.html'
    success_url = reverse_lazy('usuarios:materia-list')
    success_message = 'Materia creada correctamente.'
    extra_context = {'titulo': 'Crear Materia'}
    allowed_roles = (Usuario.Rol.ADMINISTRADOR,)


class MateriaUpdateView(RolRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Materia
    form_class = MateriaForm
    template_name = 'usuarios/form.html'
    success_url = reverse_lazy('usuarios:materia-list')
    success_message = 'Materia actualizada correctamente.'
    extra_context = {'titulo': 'Editar Materia'}
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
    form_class = AlumnoForm
    template_name = 'usuarios/form.html'
    success_url = reverse_lazy('usuarios:alumno-list')
    success_message = 'Alumno creado correctamente.'
    extra_context = {'titulo': 'Crear Alumno'}
    allowed_roles = (Usuario.Rol.ADMINISTRADOR,)


class AlumnoUpdateView(RolRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = 'usuarios/form.html'
    success_url = reverse_lazy('usuarios:alumno-list')
    success_message = 'Alumno actualizado correctamente.'
    extra_context = {'titulo': 'Editar Alumno'}
    allowed_roles = (Usuario.Rol.ADMINISTRADOR,)


class AlumnoDeleteView(RolRequiredMixin, DeleteSuccessMessageMixin, DeleteView):
    model = Alumno
    template_name = 'usuarios/confirm_delete.html'
    success_url = reverse_lazy('usuarios:alumno-list')
    success_message = 'Alumno eliminado correctamente.'
    allowed_roles = (Usuario.Rol.ADMINISTRADOR,)


class OfertaAcademicaView(RolRequiredMixin, ListView):
    model = Materia
    template_name = 'usuarios/oferta_academica.html'
    context_object_name = 'materias'
    allowed_roles = (Usuario.Rol.ALUMNO,)

    def get_queryset(self):
        alumno = self.request.user.alumno
        if not alumno or not alumno.carrera:
            return Materia.objects.none()
        return Materia.objects.filter(carrera=alumno.carrera).select_related('carrera')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        alumno = self.request.user.alumno
        if alumno:
            context['inscripciones_ids'] = set(alumno.inscripciones.values_list('materia_id', flat=True))
        else:
            context['inscripciones_ids'] = set()
        return context


class InscribirMateriaView(RolRequiredMixin, View):
    allowed_roles = (Usuario.Rol.ALUMNO,)

    def post(self, request, *args, **kwargs):
        alumno = request.user.alumno
        if not alumno or not alumno.carrera:
            messages.error(request, 'Tu usuario no tiene una carrera asignada.')
            return redirect('usuarios:oferta-academica')

        materia = get_object_or_404(Materia, pk=kwargs['pk'], carrera=alumno.carrera)
        try:
            inscribir_alumno(alumno, materia)
        except ValidationError as error:
            messages.error(request, error.message)
        else:
            messages.success(request, 'Inscripción exitosa.')

        return redirect('usuarios:oferta-academica')


class MisMateriasView(RolRequiredMixin, ListView):
    model = Inscripcion
    template_name = 'usuarios/mis_materias.html'
    context_object_name = 'inscripciones'
    allowed_roles = (Usuario.Rol.ALUMNO,)

    def get_queryset(self):
        alumno = self.request.user.alumno
        if not alumno:
            return Inscripcion.objects.none()
        return (
            Inscripcion.objects.filter(alumno=alumno)
            .select_related('materia', 'materia__carrera')
            .order_by('materia__nombre')
        )


class BajaMateriaView(RolRequiredMixin, View):
    allowed_roles = (Usuario.Rol.ALUMNO,)

    def post(self, request, *args, **kwargs):
        alumno = request.user.alumno
        if not alumno:
            messages.error(request, 'Tu usuario no tiene un perfil de alumno asociado.')
            return redirect('usuarios:mis-materias')

        inscripcion = get_object_or_404(Inscripcion, pk=kwargs['pk'], alumno=alumno)
        inscripcion.delete()
        messages.success(request, 'Te diste de baja de la materia correctamente.')

        return redirect('usuarios:mis-materias')


class MateriaInscriptosListView(RolRequiredMixin, ListView):
    model = Inscripcion
    template_name = 'usuarios/materia_inscriptos_list.html'
    context_object_name = 'inscripciones'
    allowed_roles = (Usuario.Rol.ADMINISTRADOR,)

    def dispatch(self, request, *args, **kwargs):
        self.materia = get_object_or_404(Materia, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return (
            Inscripcion.objects.filter(materia=self.materia)
            .select_related('alumno')
            .order_by('alumno__apellido', 'alumno__nombre')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['materia'] = self.materia
        return context
