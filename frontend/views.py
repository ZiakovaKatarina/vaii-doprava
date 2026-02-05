from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Max, F
from django.views.decorators.http import require_http_methods, require_GET
from users.decorators import admin_required
from django.contrib import messages
from django.db.models import ProtectedError
import json
from django.db import transaction

from data_management.models import Stop, Trip, Route, Vehicle, RouteStop
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
            return JsonResponse({'ok': True, 'redirect': '/stops/'})
        else:
            error_text = " ".join([error for field in form.errors for error in form.errors[field]])
            return JsonResponse({'ok': False, 'errors': error_text}, status=400)
    else:
        form = StopForm()
    return render(request, 'stops/stop_form.html', {'form': form, 'title': 'Pridať zastávku'})

@admin_required
def stop_update(request, pk):
    stop = get_object_or_404(Stop, pk=pk)
    if request.method == "POST":
        if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'ok': False, 'error': 'Update je povolený len cez AJAX.'}, status=403)
        form = StopForm(request.POST, instance=stop)
        if form.is_valid():
            form.save()
            return JsonResponse({'ok': True, 'redirect': '/stops/'})
        else:
            error_text = " ".join([error for field in form.errors for error in form.errors[field]])
            return JsonResponse({'ok': False, 'errors': error_text}, status=400)
    else:
        form = StopForm(instance=stop)
    return render(request, 'stops/stop_form.html', {
        'form': form,
        'stop': stop,
        'title': 'Upraviť zastávku'
    })

@admin_required
@require_http_methods(["DELETE", "POST"])
def stop_delete(request, pk):
    try:
        stop = get_object_or_404(Stop, pk=pk)
        stop.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'ok': True})
        messages.success(request, "Zastávka bola úspešne zmazaná.")
        return redirect('frontend:stop_list')
    except ProtectedError:
        error_msg = "Túto zastávku nie je možné zmazať, pretože je súčasťou jednej alebo viacerých trás (liniek). Najskôr ju odstráňte z trasy."
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'ok': False, 'error': error_msg}, status=400)
        messages.error(request, error_msg)
        return redirect('frontend:stop_list')
    except Stop.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Zastávka neexistuje'}, status=404)

@require_http_methods(['PATCH'])
@login_required
def stop_update_inline(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        return JsonResponse({'detail': 'Forbidden'}, status=403)
    
    stop = get_object_or_404(Stop, pk=pk)
    import json
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    updated = False
    if 'name' in data:
        stop.name = data['name']
        updated = True
    if 'latitude' in data:
        try:
            stop.latitude = float(data['latitude'])
            updated = True
        except ValueError:
            return JsonResponse({'error': 'Neplatná hodnota latitude'}, status=400)
    if 'longitude' in data:
        try:
            stop.longitude = float(data['longitude'])
            updated = True
        except ValueError:
            return JsonResponse({'error': 'Neplatná hodnota longitude'}, status=400)
    
    if updated:
        stop.save()
        return JsonResponse({'ok': True})
    else:
        return JsonResponse({'error': 'Žiadne zmeny'}, status=400)

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
            route = form.save()
            
            RouteStop.objects.get_or_create(route=route, stop=route.start_stop, defaults={"order": 1})
            RouteStop.objects.get_or_create(route=route, stop=route.end_stop, defaults={"order": 2})
            
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

# Connections
from django.db.models import Prefetch
from data_management.models import RouteStop

def search_connections(request):
    stops = Stop.objects.all().order_by("name")
    start_id = request.GET.get("start_stop")
    end_id = request.GET.get("end_stop")

    direct_connections = []
    transfer_connections = []
    start_stop = None
    end_stop = None

    if start_id and end_id and start_id != end_id:
        start_stop = get_object_or_404(Stop, pk=start_id)
        end_stop = get_object_or_404(Stop, pk=end_id)

        # --- PRIAME TRASY ---
        start_rss = RouteStop.objects.filter(stop=start_stop)
        for s_rs in start_rss:
            valid_ends = RouteStop.objects.filter(
                route=s_rs.route, 
                stop=end_stop, 
                order__gt=s_rs.order
            )
            
            if valid_ends.exists():
                trips = Trip.objects.filter(route=s_rs.route).select_related('vehicleID')
                if trips.exists():
                    for t in trips:
                        direct_connections.append({
                            "route": s_rs.route,
                            "trip": t,
                            "has_times": True
                        })
                else:
                    # Trasa existuje, ale bez konkrétnych spojov (Tripov)
                    direct_connections.append({
                        "route": s_rs.route,
                        "has_times": False
                    })

        # --- PRESTUPY (iba ak nie sú priame) ---
        if not direct_connections:
            seen_transfers = set()
            r1_list = RouteStop.objects.filter(stop=start_stop)
            r2_list = RouteStop.objects.filter(stop=end_stop)

            for r1 in r1_list:
                for r2 in r2_list:
                    if r1.route == r2.route:
                        continue
                    
                    common_x = RouteStop.objects.filter(
                        route=r1.route, order__gt=r1.order
                    ).values_list('stop', flat=True)

                    transfers = RouteStop.objects.filter(
                        route=r2.route, stop_id__in=common_x, order__lt=r2.order
                    ).select_related('stop')

                    for x in transfers:
                        key = (r1.route.id, x.stop.id, r2.route.id)
                        if key not in seen_transfers:
                            transfer_connections.append({
                                "stop_x": x.stop,
                                "route1": r1.route,
                                "route2": r2.route,
                            })
                            seen_transfers.add(key)

    return render(request, "search_connections.html", {
        "stops": stops,
        "direct_connections": direct_connections,
        "transfer_connections": transfer_connections,
        "start_stop": start_stop,
        "end_stop": end_stop,
    })
"""
def search_connections(request):
    stops = Stop.objects.all().order_by("name")
    start_id = request.GET.get("start_stop")
    end_id = request.GET.get("end_stop")

    direct_connections = []
    transfer_connections = []
    start_stop = None
    end_stop = None

    if start_id and end_id and start_id != end_id:
        start_stop = get_object_or_404(Stop, pk=start_id)
        end_stop = get_object_or_404(Stop, pk=end_id)

        # --- 1. PRIAME SPOJE (bez duplicit) ---
        start_rss = RouteStop.objects.filter(stop=start_stop)
        seen_direct_trips = set()

        for s_rs in start_rss:
            valid_ends = RouteStop.objects.filter(
                route=s_rs.route,
                stop=end_stop,
                order__gt=s_rs.order
            )

            if valid_ends.exists():
                trips = Trip.objects.filter(route=s_rs.route).select_related('vehicleID')
                for t in trips:
                    trip_key = (t.route_id, t.departure_time)
                    if trip_key not in seen_direct_trips:
                        direct_connections.append({
                            "route": s_rs.route,
                            "trip": t,
                            "departure": t.departure_time,
                            "arrival": t.arrival_time,
                            "vehicle": t.vehicleID,
                        })
                        seen_direct_trips.add(trip_key)

        # --- 2. PRESTUPY (len ak nie je priamy spoj) ---
        if not direct_connections:
            seen_transfers = set()

            routes_from_start = RouteStop.objects.filter(stop=start_stop)
            routes_to_end = RouteStop.objects.filter(stop=end_stop)

            for r1 in routes_from_start:
                for r2 in routes_to_end:
                    if r1.route == r2.route:
                        continue

                    common_stops = RouteStop.objects.filter(
                        route=r1.route,
                        order__gt=r1.order
                    ).values_list('stop', flat=True)

                    transfers = RouteStop.objects.filter(
                        route=r2.route,
                        stop_id__in=common_stops,
                        order__lt=r2.order
                    ).select_related('stop')

                    for x in transfers:
                        transfer_key = (r1.route.id, x.stop.id, r2.route.id)
                        if transfer_key not in seen_transfers:
                            transfer_connections.append({
                                "stop_x": x.stop,
                                "route1": r1.route,
                                "route2": r2.route,
                            })
                            seen_transfers.add(transfer_key)

    return render(request, "search_connections.html", {
        "stops": stops,
        "direct_connections": direct_connections,
        "transfer_connections": transfer_connections[:10],
        "start_id": start_id,
        "end_id": end_id,
    })
"""
@admin_required
def route_stops_manage(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    route_stops = RouteStop.objects.filter(route=route).select_related("stop").order_by("order")
    stops = Stop.objects.all().order_by("name")

    if request.method == "POST":
        stop_id = request.POST.get("stop")
        order = request.POST.get("order")

        if not stop_id:
            messages.error(request, "Vyber zastávku.")
            return redirect("frontend:route_stops_manage", route_id=route.id)

        with transaction.atomic():
            if not order:
                max_order = RouteStop.objects.filter(route=route).aggregate(Max("order"))["order__max"] or 0
                new_order = max_order + 1
            else:
                try:
                    new_order = int(order)
                    RouteStop.objects.filter(route=route, order__gte=new_order).update(order=F('order') + 1)
                except ValueError:
                    messages.error(request, "Poradie musí byť číslo.")
                    return redirect("frontend:route_stops_manage", route_id=route.id)

            RouteStop.objects.create(route=route, stop_id=stop_id, order=new_order)
            _reorder_route_stops(route)
            
        messages.success(request, "Zastávka pridaná do trasy.")
        return redirect("frontend:route_stops_manage", route_id=route.id)

    return render(request, "routes/route_stops_manage.html", {
        "route": route,
        "route_stops": route_stops,
        "stops": stops,
    })

@admin_required
def route_stops_renumber(request, route_id):
    """Renumber all stops in a route sequentially (1, 2, 3...)"""
    route = get_object_or_404(Route, pk=route_id)
    
    with transaction.atomic():
        route_stops = RouteStop.objects.filter(route=route).order_by("order")
        for idx, rs in enumerate(route_stops, start=1):
            rs.order = idx
            rs.save()
    
    messages.success(request, "Poradie zastávok bolo prečíslované.")
    return redirect("frontend:route_stops_manage", route_id=route.id)

@admin_required
def route_stop_delete(request, route_id, rs_id):
    route = get_object_or_404(Route, pk=route_id)
    rs = get_object_or_404(RouteStop, pk=rs_id, route=route)
    rs.delete()
    
    _reorder_route_stops(route)
    
    messages.success(request, "Zastávka odstránená z trasy.")
    return redirect("frontend:route_stops_manage", route_id=route.id)

def _reorder_route_stops(route):
    """Pridelí poradie 1, 2, 3... všetkým zastávkam linky."""
    with transaction.atomic():
        stops = RouteStop.objects.filter(route=route).order_by('order', 'id')
        for index, rs in enumerate(stops, start=1):
            if rs.order != index:
                rs.order = index
                rs.save(update_fields=['order'])