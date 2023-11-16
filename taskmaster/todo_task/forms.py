from django import forms
from django.forms.widgets import DateInput
from django.utils import timezone

from .models import Label, Priority, Task, TaskMetadata


class BaseTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "complete",
            "labels",
            "due_date",
        ]

        labels = {
            "title": "Título de la Tarea",
            "complete": "Completada",
            "labels": "Categorías",
            "due_date": "Fecha a realizar tarea",
        }

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Ingrese el título"}),
            "due_date": DateInput(attrs={"placeholder": "dd/mm/aaaa"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # Extraer 'user' del kwargs
        super(BaseTaskForm, self).__init__(*args, **kwargs)

        if user:
            self.fields["labels"].queryset = Label.objects.filter(user=user)

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) <= 8:
            raise forms.ValidationError("El título debe tener más de 8 caracteres.")
        return title

    def clean_due_date(self):
        due_date = self.cleaned_data["due_date"]
        if due_date and due_date < timezone.now().date():
            print(due_date)
            print(timezone.now().date())
            raise forms.ValidationError(
                "La fecha de vencimiento no puede ser en el pasado."
            )
        return due_date


class TaskForm(BaseTaskForm):
    class Meta(BaseTaskForm.Meta):
        exclude = ["complete"]


class TaskEditForm(BaseTaskForm):
    class Meta(BaseTaskForm.Meta):
        pass


class TaskMetaDataForm(forms.ModelForm):
    class Meta:
        model = TaskMetadata
        fields = ["description", "priority"]

        labels = {
            "description": "Descripcion",
            "priority": "Prioridad",
        }

        widgets = {
            "description": forms.TextInput(
                attrs={"placeholder": "Ingrese la descripción"}
            ),
        }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # Extraer 'user' del kwargs
        super(TaskMetaDataForm, self).__init__(*args, **kwargs)

        if user:
            self.fields["priority"].queryset = Priority.objects.filter(user=user)


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
