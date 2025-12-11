from django.shortcuts import render, get_object_or_404, redirect
from data_management.models import Stop, Trip, Route
from .forms import StopForm, TripForm, RouteForm

def home(request):
    return render(request, 'home.html', {})

# LIST
def stop_list(request):
    stops = Stop.objects.all().order_by('name')
    return render(request, 'stops/stop_list.html', {'stops': stops})

# CREATE
def stop_create(request):
    if request.method == "POST":
        form = StopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stop_list')
    else:
        form = StopForm()

    return render(request, 'stops/stop_form.html', {'form': form, 'title': 'Pridať zastávku'})

# UPDATE
def stop_update(request, pk):
    stop = get_object_or_404(Stop, pk=pk)
    if request.method == "POST":
        form = StopForm(request.POST, instance=stop)
        if form.is_valid():
            form.save()
            return redirect('stop_list')
    else:
        form = StopForm(instance=stop)

    return render(request, 'stops/stop_form.html', {'form': form, 'title': 'Upraviť zastávku'})

# DELETE
def stop_delete(request, pk):
    stop = get_object_or_404(Stop, pk=pk)
    if request.method == "POST":
        stop.delete()
        return redirect('stop_list')

    return render(request, 'stops/stop_confirm_delete.html', {'stop': stop})

# LIST
def trip_list(request):
    trips = Trip.objects.all().order_by('routeID')
    return render(request, 'trips/trip_list.html', {'trips': trips})

# CREATE
def trip_create(request):
    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trip_list')
    else:
        form = TripForm()

    return render(request, 'trips/trip_form.html', {'form': form, 'title': 'Pridať spoj'})

# UPDATE
def trip_update(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if request.method == "POST":
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            return redirect('trip_list')
    else:
        form = TripForm(instance=trip)

    return render(request, 'trips/trip_form.html', {'form': form, 'title': 'Upraviť zastávku'})

# DELETE
def trip_delete(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if request.method == "POST":
        trip.delete()
        return redirect('trip_list')

    return render(request, 'trips/trip_confirm_delete.html', {'trip': trip})

# LIST
def route_list(request):
    routes = Route.objects.all().order_by('name')
    return render(request, 'routes/route_list.html', {'routes': routes})

# CREATE
def route_create(request):
    if request.method == "POST":
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('route_list')
    else:
        form = RouteForm()

    return render(request, 'routes/route_form.html', {'form': form, 'title': 'Pridať linku'})

# UPDATE
def route_update(request, pk):
    route = get_object_or_404(Route, pk=pk)
    if request.method == "POST":
        form = RouteForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            return redirect('route_list')
    else:
        form = RouteForm(instance=route)

    return render(request, 'routes/route_form.html', {'form': form, 'title': 'Upraviť linku'})

# DELETE
def route_delete(request, pk):
    route = get_object_or_404(Route, pk=pk)
    if request.method == "POST":
        route.delete()
        return redirect('route_list')
    
    return render(request, 'routes/route_confirm_delete.html', {'route': route})