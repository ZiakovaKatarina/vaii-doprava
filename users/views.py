from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserProfileForm, AdminUserEditForm
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()

def register(request):
    """Registrácia nového používateľa"""
    if request.user.is_authenticated:
        messages.info(request, 'Ste už prihlásený.')
        return redirect('frontend:home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'registered'
            user.save()
            
            login(request, user)
            messages.success(request, f'Vitajte {user.first_name}! Registrácia bola úspešná.')
            return redirect('frontend:home')
        else:
            messages.error(request, 'Opravte prosím chyby vo formulári.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    """Zobrazenie profilu používateľa"""
    return render(request, 'users/profile.html', {'user': request.user})

@login_required
def profile_edit(request):
    """Úprava profilu používateľa"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'users/profile_edit.html', {'form': form})

@login_required
def users_list(request):
    """Zoznam všetkých registrovaných používateľov - iba pre admin"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Nemáte oprávnenie pristúpiť k tejto stránke.')
        return redirect('frontend:home')
    
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'users/users_list.html', {'users': users})

@login_required
def users_edit(request, pk):
    """Úprava profilu používateľa - iba admin"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Nemáte oprávnenie.')
        return redirect('frontend:home')
    
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Profil používateľa {user.username} bol aktualizovaný.')
            return redirect('users:users_list')
    else:
        form = AdminUserEditForm(instance=user)
    
    return render(request, 'users/users_edit.html', {'form': form, 'edited_user': user})

@login_required
def send_password_reset(request, pk):
    """Poslať odkaz na reset hesla - iba admin"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Nemáte oprávnenie.')
        return redirect('frontend:home')
    
    user = get_object_or_404(User, pk=pk)
    
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_link = f"http://127.0.0.1:8000/users/reset/{uid}/{token}/"
    
    send_mail(
        subject='Požiadavka na reset hesla',
        message=f'Kliknite na odkaz na reset hesla:\n{reset_link}',
        from_email='noreply@doprava.sk',
        recipient_list=[user.email],
    )
    
    messages.success(request, f'Email s resetom hesla bol odoslaný na {user.email}')
    return redirect('users:users_list')