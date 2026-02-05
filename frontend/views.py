from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Max
from django.views.decorators.http import require_http_methods, require_GET
from users.decorators import admin_required
from django.contrib import messages
from django.db.models import ProtectedError
import json

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

    connections = []
    start_stop = None
    end_stop = None

    if start_id and end_id and start_id != end_id:
        start_stop = get_object_or_404(Stop, pk=start_id)
        end_stop = get_object_or_404(Stop, pk=end_id)

        candidate_routes = Route.objects.filter(
            route_stops__stop=start_stop,
        ).filter(
            route_stops__stop=end_stop
        ).distinct()

        route_stops_map = {}
        rs_qs = RouteStop.objects.filter(route__in=candidate_routes).select_related("stop").order_by("route_id", "order")
        for rs in rs_qs:
            route_stops_map.setdefault(rs.route_id, []).append(rs.stop_id)

        valid_routes = []
        direction_map = {}

        for r in candidate_routes:
            stop_ids = route_stops_map.get(r.id, [])
            if start_stop.id not in stop_ids or end_stop.id not in stop_ids:
                continue

            i = stop_ids.index(start_stop.id)
            j = stop_ids.index(end_stop.id)

            if i < j:
                valid_routes.append(r)
                direction_map[r.id] = "tam"
            elif j < i:
                valid_routes.append(r)
                direction_map[r.id] = "späť"

        trips = Trip.objects.filter(route__in=valid_routes).select_related("route", "vehicleID").order_by("departure_time")

        for t in trips:
            stop_ids = route_stops_map.get(t.route_id, [])
            i = stop_ids.index(start_stop.id)
            j = stop_ids.index(end_stop.id)
            segment_ids = stop_ids[i:j+1] if i < j else stop_ids[j:i+1][::-1]
            stop_name_by_id = {s.id: s.name for s in Stop.objects.filter(id__in=segment_ids)}
            ordered_names = [stop_name_by_id[sid] for sid in segment_ids]

            connections.append({
                "trip": t,
                "route": t.route,
                "vehicle": t.vehicleID,
                "direction": direction_map.get(t.route_id, ""),
                "segment": ordered_names,
            })

    return render(request, "search_connections.html", {
        "stops": stops,
        "connections": connections,
        "start_id": start_id,
        "end_id": end_id,
        "start_stop": start_stop,
        "end_stop": end_stop,
    })

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

        if not order:
            max_order = RouteStop.objects.filter(route=route).aggregate(Max("order"))["order__max"] or 0
            order = max_order + 1

        try:
            order = int(order)
        except ValueError:
            messages.error(request, "Poradie musí byť číslo.")
            return redirect("frontend:route_stops_manage", route_id=route.id)

        if RouteStop.objects.filter(route=route, stop_id=stop_id).exists():
            messages.error(request, "Táto zastávka už na linke existuje.")
            return redirect("frontend:route_stops_manage", route_id=route.id)

        if RouteStop.objects.filter(route=route, order=order).exists():
            messages.error(request, f"Poradie {order} je už použité. Zvoľ iné.")
            return redirect("frontend:route_stops_manage", route_id=route.id)

        RouteStop.objects.create(route=route, stop_id=stop_id, order=order)
        messages.success(request, "Zastávka pridaná do trasy.")
        return redirect("frontend:route_stops_manage", route_id=route.id)

    return render(request, "routes/route_stops_manage.html", {
        "route": route,
        "route_stops": route_stops,
        "stops": stops,
    })

@admin_required
def route_stop_delete(request, route_id, rs_id):
    route = get_object_or_404(Route, pk=route_id)
    rs = get_object_or_404(RouteStop, pk=rs_id, route=route)
    rs.delete()
    messages.success(request, "Zastávka odstránená z trasy.")
    return redirect("frontend:route_stops_manage", route_id=route.id)