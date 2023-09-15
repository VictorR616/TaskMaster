from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from users.models import CustomUser
from users.forms import UserForm

from django.contrib.auth import login, authenticate, logout
from .decorators import admin_or_worker_required
from django.contrib.auth.decorators import login_required


@login_required(login_url='/users/login/')
@admin_or_worker_required
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

@login_required(login_url='/users/login/')
def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    return render(request, 'users/user_detail.html', {'user': user})

@login_required(login_url='/users/login/')
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'users/user_create.html', {'form': form})

@login_required(login_url='/users/login/')
def user_update(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'users/user_create.html', {'form': form, 'user': user})

@login_required(login_url='/users/login/')
def user_delete(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
        return redirect('user_list')
    return render(request, 'users/user_delete.html', {'user': user})


# Manejo de sesion
def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('user_list')
        else:
            messages.error(request, 'Credenciales incorrectas. Intente nuevamente.')

    return render(request, 'users/login.html')

def cerrar_sesion(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('login')
