from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import IntegrityError
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CategoryForm, PriorityForm, TaskEditForm, TaskForm, TaskMetaDataForm
from .models import Label, Priority, Task


@login_required(login_url="/users/login/")
def list_tasks(request, filter_type=None):
    fecha_actual = datetime.now()

    if filter_type:
        if filter_type == "complete":
            tasks = Task.objects.filter(user=request.user, complete=True)
        elif filter_type == "all":
            tasks = Task.objects.filter(user=request.user)
    else:
        tasks = Task.objects.filter(user=request.user, complete=False)

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

    # Filtrar categorías según las tareas seleccionadas
    categorias = (
        Label.objects.filter(task__user=request.user, task__in=tasks)
        .annotate(task_count=Count("task"))
        .order_by("-task_count")[:4]
    )

    context = {
        "paginator_data": paginator_data,
        "fecha_actual": fecha_actual,
        "query": query,
        "categorias": categorias,
        "placeholder": "Buscar tareas",
        "filter_type": filter_type,  # Pasa el filtro a la plantilla
    }

    return render(request, "todo_task/tasks/list.html", context)


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
        task_form = TaskForm(request.POST, user=request.user)
        task_metadata_form = TaskMetaDataForm(request.POST, user=request.user)

        if task_form.is_valid() and task_metadata_form.is_valid():
            task = task_form.save(commit=False)
            task.user = request.user
            task.save()

            task.labels.set(task_form.cleaned_data["labels"])

            task_metadata = task_metadata_form.save(commit=False)
            task_metadata.task = task
            task_metadata.save()

            return redirect("task-list")
    else:
        task_form = TaskForm(user=request.user)
        task_metadata_form = TaskMetaDataForm(user=request.user)

    context = {"task_form": task_form, "task_metadata_form": task_metadata_form}

    return render(request, "todo_task/tasks/create.html", context)


@login_required(login_url="/users/login/")
def update_task(request, task_id):
    # Obtener la tarea asociada al usuario actual
    task = get_object_or_404(Task, pk=task_id)

    if request.method == "POST":
        # Pasar el usuario actual al formulario para filtrar las opciones
        task_form = TaskEditForm(request.POST, instance=task, user=request.user)
        task_metadata_form = TaskMetaDataForm(
            request.POST, instance=task.taskmetadata, user=request.user
        )

        if task_form.is_valid() and task_metadata_form.is_valid():
            task_form.save()
            task_metadata_form.save()
            return redirect("task-list")
    else:
        # Pasar el usuario actual al formulario para filtrar las opciones
        task_form = TaskEditForm(instance=task, user=request.user)
        task_metadata_form = TaskMetaDataForm(
            instance=task.taskmetadata, user=request.user
        )

    context = {
        "task_form": task_form,
        "task_metadata_form": task_metadata_form,
        "task": task,
    }

    return render(request, "todo_task/tasks/update.html", context)


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
            category = category_form.save(commit=False)
            category.user = request.user

            try:
                category.save()
                return redirect("category-list")
            except IntegrityError:
                category_form.add_error(
                    "name", "Ya existe una etiqueta con este nombre."
                )
    else:
        category_form = CategoryForm()

    context = {"category_form": category_form}
    return render(request, "todo_task/categories/create.html", context)


@login_required(login_url="/users/login/")
def update_category(request, category_id):
    category = get_object_or_404(Label, pk=category_id)

    if request.method == "POST":
        category_form = CategoryForm(request.POST, instance=category)

        if category_form.is_valid():
            try:
                category_form.save()
                return redirect("category-list")
            except IntegrityError:
                category_form.add_error(
                    "name", "Ya existe una etiqueta con este nombre."
                )
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
            priority = priority_form.save(commit=False)
            priority.user = request.user
            try:
                priority.save()
                return redirect("priority-list")
            except IntegrityError:
                priority_form.add_error(
                    "name", "Ya existe una prioridad con este nombre."
                )
    else:
        priority_form = PriorityForm()

    context = {"priority_form": priority_form}
    return render(request, "todo_task/priorities/create.html", context)


@login_required(login_url="/users/login/")
def update_priority(request, priority_id):
    priority = get_object_or_404(Priority, pk=priority_id)

    if request.method == "POST":
        priority_form = PriorityForm(request.POST, instance=priority)

        if priority_form.is_valid():
            try:
                priority_form.save()
                return redirect("priority-list")
            except IntegrityError:
                priority_form.add_error(
                    "name", "Ya existe una prioridad con este nombre."
                )
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


def error_404(request, exception):
    return render(request, "404.html", status=404)
