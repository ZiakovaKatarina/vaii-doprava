from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    # Cesta pre http://127.0.0.1:8000/
    path('', views.home, name='home'),

    path('stops/', views.stop_list, name='stop_list'),
    path('stops/create/', views.stop_create, name='stop_create'),
    path('stops/<int:pk>/edit/', views.stop_update, name='stop_update'),
    path('stops/<int:pk>/delete/', views.stop_delete, name='stop_delete'),

    path('trips/', views.trip_list, name='trip_list'),
    path('trips/create/', views.trip_create, name='trip_create'),
    path('trips/<int:pk>/edit/', views.trip_update, name='trip_update'),
    path('trips/<int:pk>/delete/', views.trip_delete, name='trip_delete'),

    path('routes/', views.route_list, name='route_list'),
    path('routes/create/', views.route_create, name='route_create'),
    path('routes/<int:pk>/edit/', views.route_update, name='route_update'),
    path('routes/<int:pk>/delete/', views.route_delete, name='route_delete'),

    path('files/', views.file_upload, name='file_upload'),
    path('files/jdf', views.jdf_upload, name='jdf_upload'),
    path('files/gdtf', views.gdtf_upload, name='gdtf_upload'),

    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/create/', views.vehicle_create, name='vehicle_create'),
    path('vehicles/update/<int:pk>/', views.vehicle_update, name='vehicle_update'),
    path('vehicles/delete/<int:pk>/', views.vehicle_delete, name='vehicle_delete'),
]