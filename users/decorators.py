from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from functools import wraps

def admin_required(view_func):
    """Dekorátor pre views prístupné len administrátorovi"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.shortcuts import redirect
            from django.contrib import messages
            messages.error(request, 'Pre prístup k tejto stránke sa musíte prihlásiť.')
            return redirect('users:login')
        
        if not request.user.is_admin():
            raise PermissionDenied("Nemáte oprávnenie na prístup k tejto stránke.")
        
        return view_func(request, *args, **kwargs)
    return wrapper

def registered_user_required(view_func):
    """Dekorátor pre views prístupné registrovaným používateľom"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.shortcuts import redirect
            from django.contrib import messages
            messages.error(request, 'Pre prístup k tejto stránke sa musíte prihlásiť.')
            return redirect('users:login')
        
        return view_func(request, *args, **kwargs)
    return wrapper