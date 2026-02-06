from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserProfileForm, AdminUserEditForm
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse

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
            user = form.save()

            user.role = 'admin' if user.is_staff else 'registered'
            user.save(update_fields=['role'])
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

@require_POST
@login_required
def toggle_staff(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        return JsonResponse({'detail': 'Forbidden'}, status=403)

    user = get_object_or_404(User, pk=pk)
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        data = {}
    desired = bool(data.get('is_staff', False))

    if user.pk == request.user.pk:
        return JsonResponse({'detail': 'Nie je možné meniť vlastné admin oprávnenie.'}, status=400)

    if not desired and User.objects.filter(is_staff=True).exclude(pk=user.pk).count() == 0:
        return JsonResponse({'detail': 'Nemožno odobrať admin práva poslednému adminovi.'}, status=400)

    user.is_staff = desired
    user.role = 'admin' if desired else 'registered'  # sync role
    user.save(update_fields=['is_staff', 'role'])
    return JsonResponse({'ok': True, 'is_staff': user.is_staff})

@require_GET
@login_required
def users_list_api(request):

    if not (request.user.is_staff or request.user.is_superuser):
        return JsonResponse({'detail': 'Forbidden'}, status=403)

    search = (request.GET.get('search') or '').strip()
    role = request.GET.get('role')  # 'admin' | 'registered' | None
    ordering = request.GET.get('ordering') or '-date_joined'  # username | email | date_joined | -...
    page = int(request.GET.get('page') or 1)
    page_size = min(int(request.GET.get('page_size') or 10), 50)

    qs = User.objects.all()

    if search:
        qs = qs.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )

    if role == 'admin':
        qs = qs.filter(is_staff=True)
    elif role == 'registered':
        qs = qs.filter(is_staff=False)

    allowed = {'username', 'email', 'date_joined', '-username', '-email', '-date_joined'}
    if ordering not in allowed:
        ordering = '-date_joined'
    qs = qs.order_by(ordering)

    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(page)

    results = []
    for u in page_obj.object_list:
        results.append({
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'first_name': u.first_name or '',
            'last_name': u.last_name or '',
            'is_staff': u.is_staff,
            'date_joined': u.date_joined.strftime('%d.%m.%Y %H:%M'),
            'edit_url': reverse('users:users_edit', args=[u.pk]),
            'reset_url': reverse('users:send_password_reset', args=[u.pk]),
        })

    return JsonResponse({
        'items': results,
        'page': page_obj.number,
        'pages': paginator.num_pages,
        'count': paginator.count,
        'page_size': page_size,
        'current_user_id': request.user.id,
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
            if user:
                login(request, user)
                return JsonResponse({'success': True, 'redirect_url': '/'})
            else:
                return JsonResponse({'success': False, 'error': 'Nesprávne meno alebo heslo.'}, status=400)

        if user:
            login(request, user)
            return redirect('frontend:home')
        else:
            messages.error(request, 'Nesprávne prihlasovacie údaje.')
    
    return render(request, 'users/login.html')