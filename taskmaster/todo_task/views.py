from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm


def list_tasks(request):
    tasks = Task.objects.all()
    return render(request, "todo_task/list_tasks.html", {"tasks": tasks})


def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, "todo_task/task_detail.html", {"task": task})


def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("todo_task/list_tasks")
    else:
        # Mostrar el formulario vacío si es una solicitud GET
        form = TaskForm()
    return render(request, "todo_task/create_task.html", {"form": form})


def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("todo_task/list_tasks")
    else:
        form = TaskForm(instance=task)
    return render(request, "todo_task/edit_task.html", {"form": form, "task": task})


def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        task.delete()
        return redirect("list_tasks")
    return render(request, "todo_task/delete_task.html", {"task": task})
