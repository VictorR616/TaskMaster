from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CategoryForm, PriorityForm, TaskEditForm, TaskForm, TaskMetaDataForm
from .models import Label, Priority, Task


@login_required(login_url="/users/login/")
def list_tasks(request, filter_type=None):
    fecha_actual = datetime.now()
    tasks = Task.objects.filter(user=request.user)
    
    if filter_type == "complete":
        tasks = tasks.filter(complete=True)
    elif filter_type == "incomplete":
        tasks = tasks.filter(complete=False)
    elif filter_type == "today_due_date":
        today = fecha_actual.date()
        tasks = tasks.filter(due_date=today)

    query = request.GET.get("q", "")

    if query:
        tasks = tasks.filter(title__startswith=query)

    # Paginación
    page_number = request.GET.get("page", 1)  # Valor predeterminado es 1

    paginator = Paginator(tasks, 4)

    try:
        paginator_data = paginator.page(page_number)
    except PageNotAnInteger:
        paginator_data = paginator.page(1)
    except EmptyPage:
        paginator_data = paginator.page(paginator.num_pages)

    categorias = Label.objects.annotate(task_count=Count("task")).order_by(
        "-task_count"
    )[:4]

    context = {
        "paginator_data": paginator_data,
        "fecha_actual": fecha_actual,
        "query": query,
        "categorias": categorias,
        "placeholder": "Buscar tareas",
    }

    template = "todo_task/tasks/list-due-date.html"  # Plantilla predeterminada

    if filter_type == "complete":
        template = "todo_task/tasks/list-complete.html"
    elif filter_type == "incomplete":
        template = "todo_task/tasks/list-incomplete.html"
    elif filter_type is None:
        template = "todo_task/tasks/list.html"

    return render(request, template, context)


@login_required(login_url="/users/login/")
def list_tasks_all(request):
    return list_tasks(request, filter_type=None)

@login_required(login_url="/users/login/")
def list_tasks_incomplete(request):
    return list_tasks(request, filter_type="incomplete")

@login_required(login_url="/users/login/")
def list_tasks_complete(request):
    return list_tasks(request, filter_type="complete")

@login_required(login_url="/users/login/")
def list_tasks_today_due_date(request):
    return list_tasks(request, filter_type="today_due_date")



@login_required(login_url="/users/login/")
def detail_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    delete_url = reverse("task-delete", args=[task_id])

    context = {
        "task": task,
        "delete_url": delete_url,
        "task_id_for_modal": task_id,
    }

    return render(request, "todo_task/tasks/detail.html", context)


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

    return render(request, "todo_task/tasks/create.html", context)


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
        "todo_task/tasks/update.html",
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
    return render(request, "todo_task/tasks/delete.html", {"task": task})


# Categorias
@login_required(login_url="/users/login/")
def list_categories(request):
    fecha_actual = datetime.now()
    categories = Label.objects.filter(user=request.user).order_by("created")

    query = request.GET.get("q", "")

    if query:
        categories = categories.filter(name__startswith=query)

    # Paginación
    page_number = request.GET.get("page", 1)  # Valor predeterminado es 1

    paginator = Paginator(categories, 8)

    try:
        paginator_data = paginator.page(page_number)
    except PageNotAnInteger:
        paginator_data = paginator.page(1)
    except EmptyPage:
        paginator_data = paginator.page(paginator.num_pages)

    context = {
        "paginator_data": paginator_data,
        "fecha_actual": fecha_actual,
        "query": query,
        "placeholder": "Buscar categorías",
    }

    return render(request, "todo_task/categories/list.html", context)


@login_required(login_url="/users/login/")
def detail_category(request, category_id):
    category = get_object_or_404(Label, pk=category_id)
    delete_url = reverse("category-delete", args=[category_id])

    task_count = category.task_set.count()

    context = {
        "category": category,
        "delete_url": delete_url,
        "category_id_for_modal": category_id,
        "task_count": task_count,
    }

    return render(request, "todo_task/categories/detail.html", context)


@login_required(login_url="/users/login/")
def create_category(request):
    if request.method == "POST":
        category_form = CategoryForm(request.POST)

        if category_form.is_valid():
            # Asignar el usuario actual al campo 'user' del modelo de categoría
            category = category_form.save(commit=False)
            category.user = request.user  # Asigna el usuario actual
            category.save()

            return redirect("category-list")
    else:
        # Mostrar el formulario vacío si es una solicitud GET
        category_form = CategoryForm()

    context = {"category_form": category_form}

    return render(request, "todo_task/categories/create.html", context)


@login_required(login_url="/users/login/")
def update_category(request, category_id):
    category = get_object_or_404(Label, pk=category_id)

    if request.method == "POST":
        category_form = CategoryForm(request.POST, instance=category)

        if category_form.is_valid():
            category_form.save()
            return redirect("category-list")
    else:
        category_form = CategoryForm(instance=category)

    return render(
        request,
        "todo_task/categories/update.html",
        {
            "category_form": category_form,
            "category": category,
        },
    )


@login_required(login_url="/users/login/")
def delete_category(request, category_id):
    category = get_object_or_404(Label, pk=category_id)

    if request.method == "POST":
        category.delete()
        return redirect("category-list")

    return render(request, "todo_task/categories/delete.html", {"category": category})


# Prioridades
@login_required(login_url="/users/login/")
def list_priorities(request):
    fecha_actual = datetime.now()
    priorities = Priority.objects.filter(user=request.user).order_by("created")

    query = request.GET.get("q", "")

    if query:
        priorities = priorities.filter(name__startswith=query)

    # Paginación
    page_number = request.GET.get("page", 1)  # Valor predeterminado es 1

    paginator = Paginator(priorities, 8)

    try:
        paginator_data = paginator.page(page_number)
    except PageNotAnInteger:
        paginator_data = paginator.page(1)
    except EmptyPage:
        paginator_data = paginator.page(paginator.num_pages)

    context = {
        "paginator_data": paginator_data,
        "fecha_actual": fecha_actual,
        "query": query,
        "placeholder": "Buscar prioridades",
    }

    return render(request, "todo_task/priorities/list.html", context)


@login_required(login_url="/users/login/")
def detail_priority(request, priority_id):
    priority = get_object_or_404(Priority, pk=priority_id)
    delete_url = reverse("priority-delete", args=[priority_id])

    task_count = priority.taskmetadata_set.count()

    context = {
        "priority": priority,
        "delete_url": delete_url,
        "priority_id_for_modal": priority_id,
        "task_count": task_count,
    }

    return render(request, "todo_task/priorities/detail.html", context)


@login_required(login_url="/users/login/")
def create_priority(request):
    if request.method == "POST":
        priority_form = PriorityForm(request.POST)

        if priority_form.is_valid():
            # Asignar el usuario actual al campo 'user' del modelo de categoría
            priority = priority_form.save(commit=False)
            priority.user = request.user  # Asigna el usuario actual
            priority.save()

            return redirect("priority-list")
    else:
        # Mostrar el formulario vacío si es una solicitud GET
        priority_form = PriorityForm()

    context = {"priority_form": priority_form}
    return render(request, "todo_task/priorities/create.html", context)


@login_required(login_url="/users/login/")
def update_priority(request, priority_id):
    priority = get_object_or_404(Priority, pk=priority_id)

    if request.method == "POST":
        priority_form = PriorityForm(request.POST, instance=priority)

        if priority_form.is_valid():
            priority_form.save()
            return redirect("priority-list")
    else:
        priority_form = PriorityForm(instance=priority)

    return render(
        request,
        "todo_task/priorities/update.html",
        {
            "priority_form": priority_form,
            "priority": priority,
        },
    )


@login_required(login_url="/users/login/")
def delete_priority(request, priority_id):
    priority = get_object_or_404(Priority, pk=priority_id)

    if request.method == "POST":
        priority.delete()
        return redirect("priority-list")

    return render(request, "todo_task/priorities/delete.html", {"priority": priority})


@login_required(login_url="/users/login/")
def analytics(request):
    fecha_actual = datetime.now()

    # Obtén el usuario actual
    user = request.user

    # Filtra todas las tareas del usuario actual
    todas_las_tareas = Task.objects.filter(user=user)

    # Cantidad de tareas totales
    total_tareas = todas_las_tareas.count()

    # Cantidad de tareas sin completar
    tareas_sin_completar = todas_las_tareas.filter(complete=False).count()

    # Cantidad de tareas completadas
    tareas_completadas = todas_las_tareas.filter(complete=True).count()

    # Número de categorías asociadas al usuario actual
    categorias = Label.objects.filter(user=user).count()

    # Número de prioridades asociadas al usuario actual
    prioridades = Priority.objects.filter(user=user).count()

    # Pasamos los datos al template
    context = {
        "total_tareas": total_tareas,
        "tareas_sin_completar": tareas_sin_completar,
        "tareas_completadas": tareas_completadas,
        "categorias": categorias,
        "prioridades": prioridades,
        "fecha_actual": fecha_actual,
    }

    return render(request, "todo_task/tasks/analytics.html", context)
