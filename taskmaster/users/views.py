from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from users.forms import UserEditForm, UserForm
from users.models import CustomUser


# Definir una función que verifica si el usuario es un administrador
def is_admin(user):
    return user.is_authenticated and user.is_staff 


@login_required(login_url="/users/login/")
@user_passes_test(is_admin)
def list_users(request):
    users = CustomUser.objects.exclude(pk=request.user.pk)

    # Paginación
    page_number = request.GET.get("page")

    try:
        page_number = int(page_number)
    except (TypeError, ValueError):
        page_number = 1

    paginator = Paginator(users, 4)

    try:
        paginator_data = paginator.page(page_number)
    except PageNotAnInteger:
        paginator_data = paginator.page(1)
    except EmptyPage:
        paginator_data = paginator.page(1)

    return render(request, "users/list.html", {"paginator_data": paginator_data})


@login_required(login_url="/users/login/")
def detail_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    delete_url = reverse("user-delete", args=[user_id])

    context = {
        "user": user,
        "delete_url": delete_url,
        "user_id_for_modal": user_id,
    }

    return render(request, "users/detail.html", context)

@user_passes_test(is_admin)
def create_user(request):
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(
                commit=False
            )  # Evitar guardar inmediatamente en la base de datos
            user.set_password(form.cleaned_data["password"])  # Establecer la contraseña
            user.save()  # Guardar el usuario con la contraseña encriptada
            messages.success(request, "Usuario creado correctamente.")
            return redirect("user-list")
    else:
        form = UserForm()
    return render(request, "users/create.html", {"user_form": form})


@login_required(login_url="/users/login/")
def update_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == "POST":
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect("user-list")
    else:
        form = UserEditForm(instance=user)
    return render(request, "users/update.html", {"user_form": form, "user": user})


@login_required(login_url="/users/login/")
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)

    if request.method == "POST":
        # Cambiar el estado de is_active a False en lugar de eliminar al usuario
        user.is_active = False
        user.save()
        messages.success(request, "Usuario desactivado correctamente.")
        return redirect("user-list")

    return render(request, "users/delete.html", {"user": user})


@login_required(login_url="/users/login/")
@user_passes_test(is_admin)
def reactivate_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)

    if request.method == "POST":
        # Cambiar el estado de is_active a False en lugar de eliminar al usuario
        user.is_active = True
        user.save()
        messages.success(request, "Usuario reactivado correctamente.")
        return redirect("user-list")

    return render(request, "users/delete.html", {"user": user})

# Manejo de sesion


def iniciar_sesion(request):
    if request.user.is_authenticated:
        # Si el usuario ya ha iniciado sesión, redirige a la página deseada.
        return redirect("list_tasks")  # Cambia 'user_list' a la URL que desees.

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        remember = request.POST.get("remember")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            # Configura la duración de la sesión en función del checkbox "Recordarme"
            if remember:
                request.session.set_expiry(
                    1209600
                )  # Duración de la sesión en segundos (2 semanas)
            else:
                request.session.set_expiry(
                    0
                )  # La sesión expirará al cerrar el navegador

            messages.success(request, "Inicio de sesión exitoso.")
            return redirect("user-list")
        else:
            messages.error(
                request,
                "Credenciales incorrectas. Intente nuevamente.",
                extra_tags="alert-danger",
            )
    return render(request, "users/login.html")


def cerrar_sesion(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect("login")
