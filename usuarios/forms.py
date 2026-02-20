from django import forms

from .models import Alumno, Carrera, Materia


class BootstrapModelForm(forms.ModelForm):
    """Aplica clases de Bootstrap 5 a los widgets del formulario."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            current = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{current} {css_class}'.strip()


class CarreraForm(BootstrapModelForm):
    class Meta:
        model = Carrera
        fields = ['nombre', 'duracion']


class MateriaForm(BootstrapModelForm):
    class Meta:
        model = Materia
        fields = ['nombre', 'carrera', 'cupo_maximo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['carrera'].queryset = Carrera.objects.order_by('nombre')
        self.fields['carrera'].empty_label = 'Seleccioná una carrera'


class AlumnoForm(BootstrapModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido', 'dni', 'email', 'legajo', 'carrera']
