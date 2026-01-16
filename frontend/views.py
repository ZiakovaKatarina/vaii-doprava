from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_http_methods, require_GET
from users.decorators import admin_required
import json

from data_management.models import Stop, Trip, Route, Vehicle
from data_management.forms import StopForm, TripForm, RouteForm, VehicleForm

def home(request):
    return render(request, 'home.html', {})

@admin_required
def file_upload(request):
    return render(request, 'files/file_upload.html', {})

@admin_required
def jdf_upload(request):
    return render(request, 'files/jdf_upload.html', {})

@admin_required
def gdtf_upload(request):
    return render(request, 'files/gdtf_upload.html', {})

# Stops
def stop_list(request):
    stops = Stop.objects.all()
    return render(request, 'stops/stop_list.html', {'stops': stops})

@admin_required
def stop_create(request):
    if request.method == "POST":
        form = StopForm(request.POST)
        if form.is_valid():
            form.save()
            # AJAX response
            return JsonResponse({'ok': True, 'redirect': '/stops/'})
        else:
            # AJAX error response
            return JsonResponse({'ok': False, 'errors': str(form.errors)}, status=400)
    else:
        form = StopForm()
    return render(request, 'stops/stop_form.html', {'form': form, 'title': 'Pridať zastávku'})

@admin_required
def stop_update(request, pk):
    stop = get_object_or_404(Stop, pk=pk)
    if request.method == "POST":
        form = StopForm(request.POST, instance=stop)
        if form.is_valid():
            form.save()
            return redirect('frontend:stop_list')
    else:
        form = StopForm(instance=stop)
    return render(request, 'stops/stop_form.html', {'form': form, 'title': 'Upraviť zastávku'})

@admin_required
@require_http_methods(["DELETE", "POST"])
def stop_delete(request, pk):
    try:
        stop = Stop.objects.get(pk=pk)
        stop.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'ok': True})
        return redirect('frontend:stop_list')
    except Stop.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Zastávka neexistuje'}, status=404)

@require_http_methods(['PATCH'])
@login_required
def stop_update_inline(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        return JsonResponse({'ok': False, 'error': 'Forbidden'}, status=403)
    
    stop = get_object_or_404(Stop, pk=pk)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'error': 'Invalid JSON'}, status=400)
    
    if 'name' in data:
        stop.name = data['name'][:100]
    if 'location' in data:
        stop.location = data['location'][:200]
    
    stop.save()
    return JsonResponse({'ok': True})

@require_GET
def stops_api(request):
    search = (request.GET.get('search') or '').strip()
    page = int(request.GET.get('page') or 1)
    page_size = int(request.GET.get('page_size') or 10)

    qs = Stop.objects.all()
    if search:
        qs = qs.filter(
            Q(name__icontains=search) |
            Q(latitude__icontains=search) |
            Q(longitude__icontains=search)
        )
    qs = qs.order_by('name')
    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(page)

    stops = [
        {
            'id': s.id,
            'name': s.name,
            'latitude': str(s.latitude),
            'longitude': str(s.longitude)
        }
        for s in page_obj.object_list
    ]

    return JsonResponse({
        'stops': stops,
        'page': page_obj.number,
        'pages': paginator.num_pages,
    })

# Trips
def trip_list(request):
    trips = Trip.objects.all()
    return render(request, 'trips/trip_list.html', {'trips': trips})

@admin_required
def trip_create(request):
    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('frontend:trip_list')
    else:
        form = TripForm()
    return render(request, 'trips/trip_form.html', {'form': form, 'title': 'Pridať spoj'})

@admin_required
def trip_update(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if request.method == "POST":
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            return redirect('frontend:trip_list')
    else:
        form = TripForm(instance=trip)
    return render(request, 'trips/trip_form.html', {'form': form, 'title': 'Upraviť spoj'})

@admin_required
def trip_delete(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if request.method == "POST":
        trip.delete()
        return redirect('frontend:trip_list')
    return render(request, 'trips/trip_confirm_delete.html', {'trip': trip})

# Routes
def route_list(request):
    routes = Route.objects.all()
    return render(request, 'routes/route_list.html', {'routes': routes})

@admin_required
def route_create(request):
    if request.method == "POST":
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('frontend:route_list')
    else:
        form = RouteForm()
    return render(request, 'routes/route_form.html', {'form': form, 'title': 'Pridať trasu'})

@admin_required
def route_update(request, pk):
    route = get_object_or_404(Route, pk=pk)
    if request.method == "POST":
        form = RouteForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            return redirect('frontend:route_list')
    else:
        form = RouteForm(instance=route)
    return render(request, 'routes/route_form.html', {'form': form, 'title': 'Upraviť trasu'})

@admin_required
def route_delete(request, pk):
    route = get_object_or_404(Route, pk=pk)
    if request.method == "POST":
        route.delete()
        return redirect('frontend:route_list')
    return render(request, 'routes/route_confirm_delete.html', {'route': route})

# Vehicles
def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'vehicles/vehicle_list.html', {'vehicles': vehicles})

@admin_required
def vehicle_create(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('frontend:vehicle_list')
    else:
        form = VehicleForm()
    return render(request, 'vehicles/vehicle_form.html', {'form': form, 'title': 'Pridať vozidlo'})

@admin_required
def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == "POST":
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('frontend:vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'vehicles/vehicle_form.html', {'form': form, 'title': 'Upraviť vozidlo'})

@admin_required
def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == "POST":
        vehicle.delete()
        return redirect('frontend:vehicle_list')
    return render(request, 'vehicles/vehicle_confirm_delete.html', {'vehicle': vehicle})