from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CityViewSet, WeatherDataViewSet, WeatherSearchViewSet

router = DefaultRouter()
router.register(r'cities', CityViewSet)
router.register(r'weather', WeatherDataViewSet)
router.register(r'searches', WeatherSearchViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
