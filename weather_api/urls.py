from django.urls import path
from .views import get_weather, get_forecast

urlpatterns = [
    path('get-weather/', get_weather, name='get_weather'),
    path('get-forecast/', get_forecast, name='get_forecast'),
]
