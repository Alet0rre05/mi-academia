from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import AlumnoForm, CursoForm
from .models import Alumno, Curso


def inicio(request):
    contexto = {
        "total_cursos": Curso.objects.count(),
        "total_alumnos": Alumno.objects.count(),
    }
    return render(request, "academia/inicio.html", contexto)


# ----------------------------------------------------------------- CURSOS

def curso_lista(request):
    cursos = Curso.objects.all()
    filas = [
        {
            "nombre": str(c),
            "valores": [c.nombre, c.duracion_horas],
            "ver": reverse("curso_detalle", args=[c.pk]),
            "editar": reverse("curso_editar", args=[c.pk]),
            "eliminar": reverse("curso_eliminar", args=[c.pk]),
        }
        for c in cursos
    ]
    contexto = {
        "titulo": "Cursos",
        "columnas": ["Nombre", "Duración (horas)"],
        "filas": filas,
        "crear_url": reverse("curso_crear"),
        "crear_texto": "Nuevo curso",
    }
    return render(request, "academia/lista.html", contexto)


def curso_detalle(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    contexto = {
        "titulo": f"Curso: {curso.nombre}",
        "nombre": str(curso),
        "campos": [
            ("Nombre", curso.nombre),
            ("Descripción", curso.descripcion or "—"),
            ("Duración (horas)", curso.duracion_horas),
        ],
        "relacionados_titulo": "Alumnos inscriptos",
        "relacionados": [
            {"texto": str(a), "url": reverse("alumno_detalle", args=[a.pk])}
            for a in curso.alumnos.all()
        ],
        "editar_url": reverse("curso_editar", args=[curso.pk]),
        "eliminar_url": reverse("curso_eliminar", args=[curso.pk]),
        "volver_url": reverse("curso_lista"),
    }
    return render(request, "academia/detalle.html", contexto)


def curso_crear(request):
    form = CursoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        curso = form.save()
        messages.success(request, f'Curso "{curso}" creado correctamente.')
        return redirect("curso_lista")
    return render(
        request,
        "academia/formulario.html",
        {"titulo": "Nuevo curso", "form": form, "cancelar_url": reverse("curso_lista")},
    )


def curso_editar(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    form = CursoForm(request.POST or None, instance=curso)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f'Curso "{curso}" actualizado correctamente.')
        return redirect("curso_lista")
    return render(
        request,
        "academia/formulario.html",
        {"titulo": f"Editar curso: {curso}", "form": form, "cancelar_url": reverse("curso_lista")},
    )


@require_POST
def curso_eliminar(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    nombre = str(curso)
    try:
        curso.delete()
    except ProtectedError:
        messages.error(
            request,
            f'No se puede eliminar el curso "{nombre}" porque tiene alumnos inscriptos.',
        )
    else:
        messages.success(request, f'Curso "{nombre}" eliminado correctamente.')
    return redirect("curso_lista")


# ----------------------------------------------------------------- ALUMNOS

def alumno_lista(request):
    alumnos = Alumno.objects.select_related("curso")
    filas = [
        {
            "nombre": str(a),
            "valores": [str(a), a.email, a.curso.nombre, a.fecha_inscripcion],
            "ver": reverse("alumno_detalle", args=[a.pk]),
            "editar": reverse("alumno_editar", args=[a.pk]),
            "eliminar": reverse("alumno_eliminar", args=[a.pk]),
        }
        for a in alumnos
    ]
    contexto = {
        "titulo": "Alumnos",
        "columnas": ["Alumno", "Email", "Curso", "Inscripción"],
        "filas": filas,
        "crear_url": reverse("alumno_crear"),
        "crear_texto": "Nuevo alumno",
    }
    return render(request, "academia/lista.html", contexto)


def alumno_detalle(request, pk):
    alumno = get_object_or_404(Alumno.objects.select_related("curso"), pk=pk)
    contexto = {
        "titulo": f"Alumno: {alumno}",
        "nombre": str(alumno),
        "campos": [
            ("Nombre", alumno.nombre),
            ("Apellido", alumno.apellido),
            ("Email", alumno.email),
            ("Curso", alumno.curso.nombre),
            ("Fecha de inscripción", alumno.fecha_inscripcion),
        ],
        "editar_url": reverse("alumno_editar", args=[alumno.pk]),
        "eliminar_url": reverse("alumno_eliminar", args=[alumno.pk]),
        "volver_url": reverse("alumno_lista"),
    }
    return render(request, "academia/detalle.html", contexto)


def alumno_crear(request):
    form = AlumnoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        alumno = form.save()
        messages.success(request, f'Alumno "{alumno}" creado correctamente.')
        return redirect("alumno_lista")
    return render(
        request,
        "academia/formulario.html",
        {"titulo": "Nuevo alumno", "form": form, "cancelar_url": reverse("alumno_lista")},
    )


def alumno_editar(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    form = AlumnoForm(request.POST or None, instance=alumno)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f'Alumno "{alumno}" actualizado correctamente.')
        return redirect("alumno_lista")
    return render(
        request,
        "academia/formulario.html",
        {"titulo": f"Editar alumno: {alumno}", "form": form, "cancelar_url": reverse("alumno_lista")},
    )


@require_POST
def alumno_eliminar(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    nombre = str(alumno)
    alumno.delete()
    messages.success(request, f'Alumno "{nombre}" eliminado correctamente.')
    return redirect("alumno_lista")
