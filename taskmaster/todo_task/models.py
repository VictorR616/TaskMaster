from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from users.models import CustomUser  # Importa el modelo de usuario personalizado


class Label(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="categories"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "user"], name="Categoria unica para usuario"
            )
        ]

        ordering = ["-created"]

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=35)
    complete = models.BooleanField(default=False)
    due_date = models.DateField(
        help_text="Ingrese la fecha de vencimiento.",
    )
    created = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(Label)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tasks")

    def clean(self):
        if self.due_date and self.due_date < timezone.now().date():
            raise ValidationError("La fecha de vencimiento no puede ser en el pasado.")

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title


class Priority(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="priorities"
    )

    class Meta:
        verbose_name = "Priority"  # Nombre en singular
        verbose_name_plural = "Priorities"  # Nombre en plural
        ordering = ["-created"]

        constraints = [
            models.UniqueConstraint(
                fields=["name", "user"], name="Prioridad unica para usuario"
            )
        ]


    def __str__(self):
        return self.name


class TaskMetadata(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    description = models.TextField()
    priority = models.ForeignKey(
        Priority, on_delete=models.SET_NULL, null=True, default=None
    )

    def __str__(self):
        return f"Metadata for Task: {self.task.title}"
