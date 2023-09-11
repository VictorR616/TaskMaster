from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField("Label")

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title


class Label(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creation_date"]

    def __str__(self):
        return self.text


# Tabla de metadata para almacenar la descripción y prioridad de una tarea
class TaskMetadata(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    description = models.TextField()
    priority = models.CharField(max_length=20)

    def __str__(self):
        return f"Metadata for Task: {self.task.title}"
