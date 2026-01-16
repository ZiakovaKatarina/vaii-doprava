from functools import wraps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def admin_required(view_func):
    """Dekorátor pre views prístupné len administrátorovi"""
    @login_required
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Nemáte oprávnenie.')
        return redirect('frontend:home')
    return _wrapped

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