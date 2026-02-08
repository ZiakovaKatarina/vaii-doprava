from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.home, name='home'),

    path('stops/', views.stop_list, name='stop_list'),
    path('stops/create/', views.stop_create, name='stop_create'),
    path('stops/<int:pk>/update/', views.stop_update, name='stop_update'),
    path('stops/<int:pk>/delete/', views.stop_delete, name='stop_delete'),
    path('api/stops/<int:pk>/update/', views.stop_update_inline, name='stop_update_inline'),
    path('api/stops/', views.stops_api, name='stops_api'),

    path('trips/', views.trip_list, name='trip_list'),
    path('trips/create/', views.trip_create, name='trip_create'),
    path('trips/<int:pk>/update/', views.trip_update, name='trip_update'),
    path('trips/<int:pk>/delete/', views.trip_delete, name='trip_delete'),

    path('routes/', views.route_list, name='route_list'),
    path('routes/create/', views.route_create, name='route_create'),
    path('routes/<int:pk>/update/', views.route_update, name='route_update'),
    path('routes/<int:pk>/delete/', views.route_delete, name='route_delete'),
    path(
        "routes/<int:route_id>/stops/",
        views.route_stops_manage,
        name="route_stops_manage",
    ),
    path("routes/<int:route_id>/stops/renumber/", views.route_stops_renumber, name="route_stops_renumber"),
    path("routes/<int:route_id>/stops/<int:rs_id>/delete/", views.route_stop_delete, name="route_stop_delete"),
    path('routes/<int:pk>/detail/', views.route_detail, name='route_detail'),

    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/create/', views.vehicle_create, name='vehicle_create'),
    path('vehicles/<int:pk>/update/', views.vehicle_update, name='vehicle_update'),
    path('vehicles/<int:pk>/delete/', views.vehicle_delete, name='vehicle_delete'),

    path('upload/', views.file_upload, name='file_upload'),
    path('upload/csv/', views.csv_import_stops, name='csv_upload'),

    path('search/', views.search_connections, name='search_connections'),
]