from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FavouriteRoute

from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

@login_required
def favorites(request):
    """Zobrazí obľúbené trasy používateľa"""
    favourite_routes = FavouriteRoute.objects.filter(user=request.user)
    context = {
        'favourite_routes': favourite_routes
    }
    return render(request, 'personalization/favorites.html', context)

@login_required
@require_POST
def add_favorite_ajax(request):
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