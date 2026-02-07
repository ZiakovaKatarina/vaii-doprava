from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FavouriteRoute
from data_management.models import Stop
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

@login_required
def favorites(request):
    """Zobrazí obľúbené trasy používateľa s IDčkami pre linky"""
    favourite_routes = FavouriteRoute.objects.filter(user=request.user)
    
    enhanced_routes = []
    for fav in favourite_routes:
        start_stop = Stop.objects.filter(name=fav.startLocation).first()
        end_stop = Stop.objects.filter(name=fav.endLocation).first()
        
        enhanced_routes.append({
            'id': fav.id,
            'start_name': fav.startLocation,
            'end_name': fav.endLocation,
            'start_id': start_stop.id if start_stop else None,
            'end_id': end_stop.id if end_stop else None,
        })

    context = {
        'favourite_routes': enhanced_routes
    }
    return render(request, 'personalization/favorites.html', context)

@login_required
def delete_favorite(request, pk):
    """Vymazanie obľúbenej trasy"""
    fav = get_object_or_404(FavouriteRoute, pk=pk, user=request.user)
    if request.method == 'POST':
        fav.delete()
        messages.success(request, "Trasa bola odstránená z obľúbených.")
    return redirect('personalization:favorites')

@login_required
@require_POST
def add_favorite_ajax(request):
    """Pridanie obľúbenej trasy cez AJAX"""
    try:
        data = json.loads(request.body)
        start_name = data.get('start')
        end_name = data.get('end')

        if not start_name or not end_name:
            return JsonResponse({'ok': False, 'error': 'Chýbajú názvy zastávok.'}, status=400)

        obj, created = FavouriteRoute.objects.get_or_create(
            user=request.user,
            startLocation=start_name,
            endLocation=end_name
        )

        if created:
            return JsonResponse({'ok': True, 'message': 'Trasa bola uložená do obľúbených.'})
        else:
            return JsonResponse({'ok': True, 'message': 'Túto trasu už v obľúbených máte.'})

    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)