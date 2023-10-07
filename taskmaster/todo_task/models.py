from django.db import models
from users.models import CustomUser  # Importa el modelo de usuario personalizado


class Task(models.Model):
    title = models.CharField(max_length=35)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField("Label")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tasks")

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title


class Label(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="categories"
    )

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name


class Priority(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="priorities"
    )

    class Meta:
        verbose_name = "Priority"  # Nombre en singular
        verbose_name_plural = "Priorities"  # Nombre en plural
        ordering = ["-created"]

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
