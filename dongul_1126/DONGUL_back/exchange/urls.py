from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('load_latest_data/', views.latest_exchange_rates),
    path('selected_currencies/', views.selected_currencies),
]
