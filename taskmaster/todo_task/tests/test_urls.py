from django.test import SimpleTestCase
from django.urls import resolve, reverse

from todo_task.views import (
    analytics,
    create_category,
    create_priority,
    create_task,
    delete_category,
    delete_priority,
    delete_task,
    detail_category,
    detail_priority,
    detail_task,
    list_categories,
    list_priorities,
    list_tasks_all,
    list_tasks_complete,
    list_tasks_incomplete,
    list_tasks_today_due_date,
    update_category,
    update_priority,
    update_task,
)


class TestUrls(SimpleTestCase):

    def test_list_tasks_all_url_is_resolved(self):
        url = reverse('task-list')
        self.assertEquals(resolve(url).func, list_tasks_all)

    def test_list_tasks_incomplete_url_is_resolved(self):
        url = reverse('task-list-incomplete')
        self.assertEquals(resolve(url).func, list_tasks_incomplete)

    def test_list_tasks_complete_url_is_resolved(self):
        url = reverse('task-list-complete')
        self.assertEquals(resolve(url).func, list_tasks_complete)

    def test_list_tasks_today_due_date_url_is_resolved(self):
        url = reverse('task-list-today-due-date')
        self.assertEquals(resolve(url).func, list_tasks_today_due_date)

    def test_detail_task_url_is_resolved(self):
        url = reverse('task-detail', args=[1])
        self.assertEquals(resolve(url).func, detail_task)

    def test_create_task_url_is_resolved(self):
        url = reverse('task-create')
        self.assertEquals(resolve(url).func, create_task)

    def test_update_task_url_is_resolved(self):
        url = reverse('task-update', args=[1])
        self.assertEquals(resolve(url).func, update_task)

    def test_delete_task_url_is_resolved(self):
        url = reverse('task-delete', args=[1])
        self.assertEquals(resolve(url).func, delete_task)

    def test_list_categories_url_is_resolved(self):
        url = reverse('category-list')
        self.assertEquals(resolve(url).func, list_categories)

    def test_detail_category_url_is_resolved(self):
        url = reverse('category-detail', args=[1])
        self.assertEquals(resolve(url).func, detail_category)

    def test_create_category_url_is_resolved(self):
        url = reverse('category-create')
        self.assertEquals(resolve(url).func, create_category)

    def test_update_category_url_is_resolved(self):
        url = reverse('category-update', args=[1])
        self.assertEquals(resolve(url).func, update_category)

    def test_delete_category_url_is_resolved(self):
        url = reverse('category-delete', args=[1])
        self.assertEquals(resolve(url).func, delete_category)

    def test_list_priorities_url_is_resolved(self):
        url = reverse('priority-list')
        self.assertEquals(resolve(url).func, list_priorities)

    def test_detail_priority_url_is_resolved(self):
        url = reverse('priority-detail', args=[1])
        self.assertEquals(resolve(url).func, detail_priority)

    def test_create_priority_url_is_resolved(self):
        url = reverse('priority-create')
        self.assertEquals(resolve(url).func, create_priority)

    def test_update_priority_url_is_resolved(self):
        url = reverse('priority-update', args=[1])
        self.assertEquals(resolve(url).func, update_priority)

    def test_delete_priority_url_is_resolved(self):
        url = reverse('priority-delete', args=[1])
        self.assertEquals(resolve(url).func, delete_priority)

    def test_analytics_url_is_resolved(self):
        url = reverse('analytics')
        self.assertEquals(resolve(url).func, analytics)


    # Ejemplo si la vista fuese una clase
    # def test_list_tasks_url_is_resolved(self):
    #     url = reverse('list_tasks')
    #     self.assertEquals(resolve(url).func.view_class, list_tasks)


