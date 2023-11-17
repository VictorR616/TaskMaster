from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from users.models import CustomUser


class Label(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Nombre",
        help_text="Ingrese el nombre de la etiqueta.",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación",
        help_text="Fecha y hora en que la etiqueta fue creada.",
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="Usuario",
        help_text="Usuario al que pertenece la etiqueta.",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "user"],
                name="Categoria unica para usuario",
            )
        ]

        ordering = ["-created"]
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(
        max_length=35,
        verbose_name="Título",
        help_text="Ingrese el título de la tarea.",
    )
    complete = models.BooleanField(
        default=False,
        verbose_name="Completa",
        help_text="Indica si la tarea está completa o no.",
    )
    due_date = models.DateField(
        help_text="Ingrese la fecha de vencimiento, utilice este formato dd/mm/aaaa.",
        verbose_name="Fecha de Vencimiento",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación",
        help_text="Fecha y hora en que la tarea fue creada.",
    )
    labels = models.ManyToManyField(
        Label,
        verbose_name="Etiquetas",
        help_text="Seleccione las etiquetas asociadas a la tarea.",
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Usuario",
        help_text="Usuario al que pertenece la tarea.",
    )

    def clean(self):
        if self.due_date and self.due_date < timezone.now().date():
            raise ValidationError("La fecha de vencimiento no puede ser en el pasado.")

    class Meta:
        ordering = ["-created"]
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"

    def __str__(self):
        return self.title


class Priority(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Nombre",
        help_text="Ingrese el nombre de la prioridad.",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación",
        help_text="Fecha y hora en que la prioridad fue creada.",
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="priorities",
        verbose_name="Usuario",
        help_text="Usuario al que pertenece la prioridad.",
    )

    class Meta:
        verbose_name = "Prioridad"
        verbose_name_plural = "Prioridades"
        ordering = ["-created"]

        constraints = [
            models.UniqueConstraint(
                fields=["name", "user"],
                name="Prioridad unica para usuario",
            )
        ]

    def __str__(self):
        return self.name


class TaskMetadata(models.Model):
    task = models.OneToOneField(
        Task,
        on_delete=models.CASCADE,
        verbose_name="Tarea",
        help_text="Tarea a la que pertenece esta metadata.",
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Ingrese la descripción de la metadata de la tarea.",
    )
    priority = models.ForeignKey(
        Priority,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name="Prioridad",
        help_text="Seleccione la prioridad asociada a la tarea.",
    )

    def __str__(self):
        return f"Metadata para Tarea: {self.task.title}"

    class Meta:
        verbose_name = "Metadata de Tarea"
        verbose_name_plural = "Metadata de Tareas"
