from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from users.models import CustomUser
from users.forms import UserForm

from django.contrib.auth import login, authenticate, logout, views as auth_views
from .decorators import admin_or_worker_required
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator




@login_required(login_url="/users/login/")
@admin_or_worker_required
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, "users/user_list.html", {"users": users})


@login_required(login_url="/users/login/")
def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    return render(request, "users/user_detail.html", {"user": user})


def user_create(request):
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(
                commit=False
            )  # Evitar guardar inmediatamente en la base de datos
            user.set_password(form.cleaned_data["password"])  # Establecer la contraseña
            user.save()  # Guardar el usuario con la contraseña encriptada
            messages.success(request, "Usuario creado correctamente.")
            return redirect("user_list")
    else:
        form = UserForm()
    return render(request, "users/user_create.html", {"user_form": form})


@login_required(login_url="/users/login/")
def user_update(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect("user_list")
    else:
        form = UserForm(instance=user)
    return render(request, "users/user_update.html", {"user_form": form, "user": user})


@login_required(login_url="/users/login/")
def user_delete(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == "POST":
        user.delete()
        messages.success(request, "Usuario eliminado correctamente.")
        return redirect("user_list")
    return render(request, "users/user_delete.html", {"user": user})


# Manejo de sesion


def iniciar_sesion(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        remember = request.POST.get(
            "remember"
        )  # Obtiene el valor del checkbox "Recordarme"

        print(f"Email ingresado: {email}")
        print(f"Contraseña ingresada: {password}")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            print(f"Usuario autenticado: {user}")

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
            return redirect("user_list")
        else:
            print("Autenticación fallida.")
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

