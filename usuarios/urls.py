from django.urls import path

from . import views

app_name = 'usuarios'

urlpatterns = [
    path('carreras/', views.CarreraListView.as_view(), name='carrera-list'),
    path('carreras/nueva/', views.CarreraCreateView.as_view(), name='carrera-create'),
    path('carreras/<int:pk>/editar/', views.CarreraUpdateView.as_view(), name='carrera-update'),
    path('carreras/<int:pk>/eliminar/', views.CarreraDeleteView.as_view(), name='carrera-delete'),
    path('materias/', views.MateriaListView.as_view(), name='materia-list'),
    path('materias/nueva/', views.MateriaCreateView.as_view(), name='materia-create'),
    path('materias/<int:pk>/editar/', views.MateriaUpdateView.as_view(), name='materia-update'),
    path('materias/<int:pk>/eliminar/', views.MateriaDeleteView.as_view(), name='materia-delete'),
    path('materias/<int:pk>/inscriptos/', views.MateriaInscriptosListView.as_view(), name='materia-inscriptos'),
    path('alumnos/', views.AlumnoListView.as_view(), name='alumno-list'),
    path('alumnos/nuevo/', views.AlumnoCreateView.as_view(), name='alumno-create'),
    path('alumnos/<int:pk>/editar/', views.AlumnoUpdateView.as_view(), name='alumno-update'),
    path('alumnos/<int:pk>/eliminar/', views.AlumnoDeleteView.as_view(), name='alumno-delete'),
    path('oferta-academica/', views.OfertaAcademicaView.as_view(), name='oferta-academica'),
    path('oferta-academica/<int:pk>/inscribir/', views.InscribirMateriaView.as_view(), name='materia-inscribir'),
    path('mis-materias/', views.MisMateriasView.as_view(), name='mis-materias'),
    path('mis-materias/<int:pk>/baja/', views.BajaMateriaView.as_view(), name='materia-baja'),
]
