from django.test import Client, TestCase
from django.urls import reverse
from users.models import CustomUser

from todo_task.models import Priority


class TestViews(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        # Crear un usuario de prueba y autenticarlo
        self.user = CustomUser.objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.client.login(email='testuser@gmail.com', password='testpassword')
        
        # Crear una prioridad asociada al usuario de prueba
        self.priority = Priority.objects.create(name='Alta', user=self.user)
        
        self.list_url = reverse('priority-list')
        self.detail_url = reverse('priority-detail', args=['1'])
        self.create_url = reverse('priority-create')
        self.delete_url = reverse('priority-delete', args=[self.priority.id])
        self.update_url = reverse('priority-update', args=[self.priority.id])


    def test_list_priorities(self):
        response = self.client.get(self.list_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_task/priorities/list.html')

    def test_detail_priorities(self):
        
        response = self.client.get(self.detail_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_task/priorities/detail.html')

    def test_update_priorities(self):
        response = self.client.post(self.update_url, {
            'name': 'Baja'
        })

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/todo_task/priorities/')  # Verifica la URL de redirección

        updated_priority = Priority.objects.get(id=self.priority.id)
        self.assertEqual(updated_priority.name, 'Baja')
        self.assertEqual(updated_priority.user, self.user)

        response = self.client.get('/todo_task/priorities/')  
        # Verificar que la vista use la plantilla correcta
        self.assertTemplateUsed(response, 'todo_task/priorities/list.html')


    def test_create_priorities(self):
        # Crear una prioridad directamente en la base de datos
        priority_count_before = Priority.objects.count()
        response = self.client.post(self.create_url, {
            'name': "Prioridad absoluta no encontrada"
        })

        # Verificar que la respuesta sea una redirección después de la creación exitosa
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/todo_task/priorities/')  # Verifica la URL de redirección

        # Verificar que el número de prioridades en la base de datos haya aumentado en 1
        priority_count_after = Priority.objects.count()
        self.assertEquals(priority_count_after, priority_count_before + 1)

        # Obtener la última prioridad creada
        created_priority = Priority.objects.latest('created')

        # Verificar que la prioridad se haya asociado al usuario actual
        self.assertEqual(created_priority.user, self.user)

        response = self.client.get('/todo_task/priorities/')  
        # Verificar que la vista use la plantilla correcta
        self.assertTemplateUsed(response, 'todo_task/priorities/list.html')

    def test_create_priorities_no_data(self):
        # Obtener el número de prioridades antes de la prueba
        priority_count_before = Priority.objects.count()

        # Realizar una solicitud POST vacía
        response = self.client.post(self.create_url)

        # Verificar que la respuesta sea un código de estado 400 (Bad Request)
        self.assertEquals(response.status_code, 400)

        # Obtener el número de prioridades después de la prueba
        priority_count_after = Priority.objects.count()

        # Verificar que el número de prioridades en la base de datos no haya cambiado
        self.assertEquals(priority_count_after, priority_count_before)
    
    def test_delete_priority_no_id(self):
        self.delete_url = reverse('priority-delete', args=[0])  

        # Obtener el número de prioridades antes de la eliminación
        priority_count_before = Priority.objects.count()

        # Realizar una solicitud POST para eliminar la prioridad sin proporcionar un ID válido
        response = self.client.post(self.delete_url)  # Nota que aquí no proporcionamos un ID válido

        # Verificar que la respuesta sea una redirección debido a la falta de un ID válido
        self.assertEquals(response.status_code, 404)

        # Obtener el número de prioridades después de la eliminación (que no debería cambiar)
        priority_count_after = Priority.objects.count()

        # Verificar que el número de prioridades en la base de datos sigue siendo el mismo
        self.assertEquals(priority_count_after, priority_count_before)