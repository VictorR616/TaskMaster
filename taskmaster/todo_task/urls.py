from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_tasks, name="list_tasks"),
    path("create/", views.create_task, name="create_task"),
    path("detail/<int:task_id>/", views.task_detail, name="task_detail"),
    path("update/<int:task_id>/", views.edit_task, name="edit_task"),
    path("delete/<int:task_id>/", views.delete_task, name="delete_task"),
    
]
