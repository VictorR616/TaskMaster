# decorators.py

from django.shortcuts import redirect

def admin_or_worker_required(view_func):
    """
    Decorador personalizado para restringir el acceso a administradores o trabajadores.
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff or request.user.is_worker:
            return view_func(request, *args, **kwargs)
        else:
            # Redirige al inicio de sesión si el usuario no está autorizado
            return redirect('login')
    return _wrapped_view