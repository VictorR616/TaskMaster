from django.urls import path

from . import views

urlpatterns = [
    # Tasks URLS
path("tasks/", views.list_tasks, name="task-list"),
    path("tasks/create/", views.create_task, name="task-create"),
    path("tasks/<int:task_id>/", views.detail_task, name="task-detail"),
    path("tasks/<int:task_id>/update/", views.update_task, name="task-update"),
    path("tasks/<int:task_id>/delete/", views.delete_task, name="task-delete"),
    path("tasks/filtered/<str:filter_type>/", views.list_tasks, name="task-list-with-filter"),
    # Categories URLS
    path("categories/", views.list_categories, name="category-list"),
    path("categories/create/", views.create_category, name="category-create"),
    path(
        "categories/<int:category_id>/", views.detail_category, name="category-detail"
    ),
    path(
        "categories/<int:category_id>/update/",
        views.update_category,
        name="category-update",
    ),
    path(
        "categories/<int:category_id>/delete/",
        views.delete_category,
        name="category-delete",
    ),
    # Priorities URLS
    path("priorities/", views.list_priorities, name="priority-list"),
    path("priorities/create/", views.create_priority, name="priority-create"),
    path(
        "priorities/<int:priority_id>/", views.detail_priority, name="priority-detail"
    ),
    path(
        "priorities/<int:priority_id>/update/",
        views.update_priority,
        name="priority-update",
    ),
    path(
        "priorities/<int:priority_id>/delete/",
        views.delete_priority,
        name="priority-delete",
    ),
    # Analiticas
    path("analytics/", views.analytics, name="analytics"),
]
