from django.core.validators import MinValueValidator
from django.db import models


class Curso(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    duracion_horas = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="duración (horas)",
    )

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Alumno(models.Model):
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    fecha_inscripcion = models.DateField(auto_now_add=True, verbose_name="fecha de inscripción")
    curso = models.ForeignKey(
        Curso,
        on_delete=models.PROTECT,
        related_name="alumnos",
    )

    class Meta:
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"
