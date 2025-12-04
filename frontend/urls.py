from django.urls import path
from . import views

urlpatterns = [
    # Cesta pre http://127.0.0.1:8000/
    path('', views.home, name='home'),
]