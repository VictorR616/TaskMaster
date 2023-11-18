from django.test import TestCase
from users.models import CustomUser

from todo_task.forms import BaseTaskForm, CategoryForm, PriorityForm
from todo_task.models import Label


class TestBaseTaskForm(TestCase):
    def setUp(self):
        # Crea un objeto Label para usar como clave foránea en el formulario
        self.user = CustomUser.objects.create(email="ejemplo@gmail.com", password="prueba123")
        self.label = Label.objects.create(name="Categoria de prueba", user=self.user)

    def test_valid_form_data(self):
        form = BaseTaskForm(data={
            "title": "Título de la tarea",
            "complete": False,
            "labels": [self.label.id,],  
            "due_date": "12/12/2024",
        })

        self.assertTrue(form.is_valid())

    def test_invalid_form_data(self):
        form = BaseTaskForm(data={
            "title": "Título corto",  # Título demasiado corto
            "complete": True,  # Puede ser válido, pero usamos un valor diferente para la prueba
            "labels": self.label.id,  # Usa el ID del objeto Label creado en setUp
            "due_date": "2023-10-30",  # Una fecha válida
        })

        self.assertFalse(form.is_valid())

class TestCategoryForm(TestCase):

    def test_category_form_valid_data(self):
        form = CategoryForm(data={'name': 'test'})
        self.assertTrue(form.is_valid())

    def test_category_form_no_data(self):
        form = CategoryForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

class TestPriorityForm(TestCase):

    def test_priority_form_valid_data(self):
        form = PriorityForm(data={'name': 'test'})
        self.assertTrue(form.is_valid())

    def test_priority_form_no_data(self):
        form = PriorityForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

