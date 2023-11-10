from django.test import TestCase
from users.models import CustomUser

from todo_task.models import Priority


class PriorityModelTest(TestCase):
    def setUp(self):
        # Crea un usuario de prueba
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='testpassword')

    def test_create_priority(self):
        # Crea una instancia de Priority
        priority = Priority.objects.create(name='Alta', user=self.user)

        # Verifica que la instancia se haya creado correctamente
        self.assertEqual(priority.name, 'Alta')
        self.assertEqual(priority.user, self.user)

    def test_priority_str(self):
        # Crea una instancia de Priority
        priority = Priority.objects.create(name='Baja', user=self.user)

        # Verifica que el método __str__ devuelve el nombre de la prioridad
        self.assertEqual(str(priority), 'Baja')

    def test_priority_ordering(self):
        # Crea varias instancias de Priority con diferentes fechas de creación
        Priority.objects.create(name='Alta', user=self.user)
        Priority.objects.create(name='Media', user=self.user)
        Priority.objects.create(name='Baja', user=self.user)

        # Obtiene las prioridades ordenadas por fecha de creación descendente
        priorities = Priority.objects.all()

        # Verifica que las prioridades estén ordenadas correctamente
        self.assertEqual(priorities[0].name, 'Alta')
        self.assertEqual(priorities[1].name, 'Media')
        self.assertEqual(priorities[2].name, 'Baja')

    # Puedes agregar más pruebas según tus necesidades, como validaciones, relaciones, etc.
