from django import forms

from .models import Alumno, Curso


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ["nombre", "descripcion", "duracion_horas"]
        widgets = {"descripcion": forms.Textarea(attrs={"rows": 4})}


class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ["nombre", "apellido", "email", "curso"]
