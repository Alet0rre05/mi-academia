from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    # Cursos
    path("cursos/", views.curso_lista, name="curso_lista"),
    path("cursos/nuevo/", views.curso_crear, name="curso_crear"),
    path("cursos/<int:pk>/", views.curso_detalle, name="curso_detalle"),
    path("cursos/<int:pk>/editar/", views.curso_editar, name="curso_editar"),
    path("cursos/<int:pk>/eliminar/", views.curso_eliminar, name="curso_eliminar"),
    # Alumnos
    path("alumnos/", views.alumno_lista, name="alumno_lista"),
    path("alumnos/nuevo/", views.alumno_crear, name="alumno_crear"),
    path("alumnos/<int:pk>/", views.alumno_detalle, name="alumno_detalle"),
    path("alumnos/<int:pk>/editar/", views.alumno_editar, name="alumno_editar"),
    path("alumnos/<int:pk>/eliminar/", views.alumno_eliminar, name="alumno_eliminar"),
]
