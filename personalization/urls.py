from django.urls import path
from . import views

app_name = 'personalization'

urlpatterns = [
    path('favorites/', views.favorites, name='favorites'),
    path('add-favorite-ajax/', views.add_favorite_ajax, name='add_favorite_ajax'),
    path('delete/<int:pk>/', views.delete_favorite, name='delete_favorite'),
]