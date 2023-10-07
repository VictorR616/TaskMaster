from django import forms

from .models import Label, Priority, Task, TaskMetadata


class BaseTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "complete",
            "labels",
        ]

        labels = {
            "title": "Título de la Tarea",
            "complete": "Completada",
            "labels": "Categorias",
            # Otras etiquetas personalizadas si las tienes
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) <= 8:
            raise forms.ValidationError("El título debe tener más de 8 caracteres.")
        return title


class TaskForm(BaseTaskForm):
    class Meta(BaseTaskForm.Meta):
        # Excluir el campo 'complete' en TaskForm
        exclude = ["complete"]

        # Puedes agregar campos adicionales o personalizaciones aquí si es necesario


class TaskEditForm(BaseTaskForm):
    class Meta(BaseTaskForm.Meta):
        fields = [
            "title",
            "complete",
            "labels",
        ]

    # Puedes agregar validaciones específicas para TaskEditForm aquí si es necesario


class TaskMetaDataForm(forms.ModelForm):
    class Meta:
        model = TaskMetadata
        fields = ["description", "priority"]

        labels = {
            "description": "Descripcion",
            "priority": "Prioridad",
            # Otras etiquetas personalizadas si las tienes
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = [
            "name",
        ]
        labels = {
            "name": "Nombre",
        }


class PriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = [
            "name",
        ]
        labels = {
            "name": "Prioridad",
        }
