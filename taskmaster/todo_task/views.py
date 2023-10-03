from django.shortcuts import render, redirect, get_object_or_404

from .models import Task, TaskMetadata, Label
from .forms import TaskEditForm, TaskForm, TaskMetaDataForm
from django.core.paginator import Paginator, EmptyPage
from datetime import datetime
from django.db.models import Count



from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage

def list_tasks(request):
    fecha_actual = datetime.now()
    
    tasks = Task.objects.all()
    query = request.GET.get('q', '')

    if not query:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(title__startswith=query)
    
    # Agregar paginación
    page_number = request.GET.get('page')

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
    categorias = Label.objects.annotate(task_count=Count('task'))
    
    context = {
        "tasks": tasks,
        'fecha_actual': fecha_actual,
        "query": query,
        "categorias": categorias
    }
    
    return render(request, "todo_task/list_tasks.html", context)




def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, "todo_task/task_detail.html", {"task": task})


def create_task(request):
    if request.method == "POST":
        task_form = TaskForm(request.POST)
        task_metadata_form = TaskMetaDataForm(request.POST)

        if task_form.is_valid() and task_metadata_form.is_valid():
            # Guardar la tarea (Task)
            task = task_form.save()

            # Guardar la metadata (TaskMetadata)
            task_metadata = task_metadata_form.save(commit=False)
            task_metadata.task = task  # Establecer la relación con la tarea
            task_metadata.save()

            return redirect("list_tasks")  # Redirigir a la lista de tareas
    else:
        # Mostrar los formularios vacíos si es una solicitud GET
        task_form = TaskForm()
        task_metadata_form = TaskMetaDataForm()

    context = {
        "task_form": task_form, 
        "task_metadata_form": task_metadata_form
        }
    

    return render(request, "todo_task/create_task.html", context )


def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == "POST":
        task_form = TaskEditForm(request.POST, instance=task)
        task_metadata_form = TaskMetaDataForm(request.POST, instance=task.taskmetadata)


        if task_form.is_valid() and task_metadata_form.is_valid():
            task_form.save()
            task_metadata_form.save()
            return redirect("list_tasks")
    else:
        task_form = TaskEditForm(instance=task)
        task_metadata_form = TaskMetaDataForm(instance=task.taskmetadata)

    return render(request, "todo_task/edit_task.html", {"task_form": task_form, "task_metadata_form": task_metadata_form, "task": task})


def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        task.delete()
        return redirect("list_tasks")
    return render(request, "todo_task/delete_task.html", {"task": task})

