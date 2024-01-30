# decorators.py
from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import redirect


def employer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            # Redirige al usuario no autenticado a la página de inicio de sesión
            return redirect('home')
        elif user.user_type != 'employer':
            # Si el usuario no es un empleador, muestra un mensaje de error
            return HttpResponseForbidden("No tienes permiso para ver esta página")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def developer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            # Redirige al usuario no autenticado a la página de inicio de sesión
            return redirect('home')
        elif user.user_type != 'developer':
            # Si el usuario no es un desarrollador, muestra un mensaje de error
            return HttpResponseForbidden("No tienes permiso para ver esta página")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
