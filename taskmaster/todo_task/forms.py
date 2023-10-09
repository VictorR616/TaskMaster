from django import forms

from .models import Label, Priority, Task, TaskMetadata


class BaseTaskForm(forms.ModelForm):
    # error_css_class = 'error-field' Indica la clase que ocupa el error del input
    # required_css_class = 'required-field' Indica la clase del input
    # title = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "placeholder": "Título de la Tarea"}
    #     )
    # )

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
            "due_date": forms.DateInput(
                attrs={"type": "date", "placeholder": "Seleccione la fecha"}
            ),
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
