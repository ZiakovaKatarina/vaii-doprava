from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FavouriteRoute

@login_required
def favorites(request):
    """Zobrazí obľúbené trasy používateľa"""
    favourite_routes = FavouriteRoute.objects.filter(user=request.user)
    context = {
        'favourite_routes': favourite_routes
    }
    return render(request, 'personalization/favorites.html', context)
