from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import TaskEditForm, TaskForm, TaskMetaDataForm
from .models import Label, Task


@login_required(login_url="/users/login/")
def list_tasks(request):
    fecha_actual = datetime.now()
    # Obtener las tareas del usuario actual
    tasks = Task.objects.filter(user=request.user).order_by("created")

    query = request.GET.get("q", "")

    if query:
        tasks = tasks.filter(title__startswith=query)

    # Agregar paginación
    page_number = request.GET.get("page")

    try:
        page_number = int(page_number)
    except (TypeError, ValueError):
        page_number = 1

    paginator = Paginator(tasks, 4)

    try:
        tasks = paginator.page(page_number)
    except EmptyPage:
        tasks = paginator.page(1)

    # Obtener el conteo de tareas por categoría
    categorias = Label.objects.annotate(task_count=Count("task"))

    context = {
        "tasks": tasks,
        "fecha_actual": fecha_actual,
        "query": query,
        "categorias": categorias,
    }

    return render(request, "todo_task/list.html", context)


@login_required(login_url="/users/login/")
def detail_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    delete_url = reverse("task-delete", args=[task_id])

    context = {
        "task": task,
        "delete_url": delete_url,
        "task_id_for_modal": task_id,
    }

    return render(request, "todo_task/detail.html", context)


@login_required(login_url="/users/login/")
def create_task(request):
    if request.method == "POST":
        task_form = TaskForm(request.POST)
        task_metadata_form = TaskMetaDataForm(request.POST)

        if task_form.is_valid() and task_metadata_form.is_valid():
            # Guardar la tarea (Task)
            task = task_form.save(commit=False)  # No guardar la tarea de inmediato
            task.user = request.user  # Asignar el usuario actual
            task.save()

            # Guardar la metadata (TaskMetadata)
            task_metadata = task_metadata_form.save(commit=False)
            task_metadata.task = task  # Establecer la relación con la tarea
            task_metadata.save()

            return redirect("task-list")  # Redirigir a la lista de tareas
    else:
        # Mostrar los formularios vacíos si es una solicitud GET
        task_form = TaskForm()
        task_metadata_form = TaskMetaDataForm()

    context = {"task_form": task_form, "task_metadata_form": task_metadata_form}

    return render(request, "todo_task/create.html", context)


@login_required(login_url="/users/login/")
def update_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == "POST":
        task_form = TaskEditForm(request.POST, instance=task)
        task_metadata_form = TaskMetaDataForm(request.POST, instance=task.taskmetadata)

        if task_form.is_valid() and task_metadata_form.is_valid():
            task_form.save()
            task_metadata_form.save()
            return redirect("task-list")
    else:
        task_form = TaskEditForm(instance=task)
        task_metadata_form = TaskMetaDataForm(instance=task.taskmetadata)

    return render(
        request,
        "todo_task/update.html",
        {
            "task_form": task_form,
            "task_metadata_form": task_metadata_form,
            "task": task,
        },
    )


@login_required(login_url="/users/login/")
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        task.delete()
        return redirect("task-list")
    return render(request, "todo_task/delete.html", {"task": task})
