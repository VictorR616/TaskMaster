from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from users.models import CustomUser
from users.forms import UserForm

def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    return render(request, 'users/user_detail.html', {'user': user})

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

def user_delete(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
        return redirect('user_list')
    return render(request, 'users/user_delete.html', {'user': user})
