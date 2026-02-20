from django.core.exceptions import ValidationError

from .models import Inscripcion


def inscribir_alumno(alumno, materia):
    ya_inscripto = Inscripcion.objects.filter(alumno=alumno, materia=materia).exists()
    if ya_inscripto:
        raise ValidationError('El alumno ya está inscrito en esta materia.')

    cupos_ocupados = Inscripcion.objects.filter(materia=materia).count()
    if cupos_ocupados >= materia.cupo_maximo:
        raise ValidationError('No hay cupo disponible para la materia seleccionada.')

    return Inscripcion.objects.create(alumno=alumno, materia=materia)
