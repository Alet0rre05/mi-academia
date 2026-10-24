from django.contrib import admin

from .models import Alumno, Curso

admin.site.register(Curso)
admin.site.register(Alumno)
