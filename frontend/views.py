from django.shortcuts import render, get_object_or_404, redirect
from data_management.models import Stop
from .forms import StopForm

def home(request):
    return render(request, 'home.html', {})

# LIST
def stop_list(request):
    stops = Stop.objects.all().order_by('name')
    return render(request, 'stop_list.html', {'stops': stops})

# CREATE
def stop_create(request):
    if request.method == "POST":
        form = StopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stop_list')
    else:
        form = StopForm()

    return render(request, 'stop_form.html', {'form': form, 'title': 'Pridať zastávku'})

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

    return render(request, 'stop_form.html', {'form': form, 'title': 'Upraviť zastávku'})

# DELETE
def stop_delete(request, pk):
    stop = get_object_or_404(Stop, pk=pk)
    if request.method == "POST":
        stop.delete()
        return redirect('stop_list')

    return render(request, 'stop_confirm_delete.html', {'stop': stop})