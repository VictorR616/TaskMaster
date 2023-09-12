from django import forms
from .models import Task  # Importa el modelo si es necesario


from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "complete",
            "labels",
        ]

    # Personaliza las etiquetas de los campos
    labels = {
        'title': 'Título de la Tarea',
        # Otras etiquetas personalizadas si las tienes
    }

    # Personaliza los widgets de los campos
    widgets = {
        'title': forms.Textarea(attrs={'class': 'custom-input'}),
        'complete': forms.CheckboxInput(attrs={'class': 'custom-checkbox'}),
    }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) <= 8:
            raise forms.ValidationError("El título debe tener más de 8 caracteres.")
        return title
