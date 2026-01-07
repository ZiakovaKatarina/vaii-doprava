from django.urls import path
from . import views

app_name = 'personalization'

urlpatterns = [
    path('favorites/', views.favorites, name='favorites'),
]