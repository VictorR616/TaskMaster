from django import forms
from .models import Task  # Importa el modelo si es necesario


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task  # Asocia el formulario a un modelo
        fields = [
            "title",
            "complete",
            "labels",
        ]  # Especifica los campos del modelo a incluir en el formulario
