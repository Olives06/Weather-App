from rest_framework import serializers
from .models import City, WeatherData, WeatherSearch

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'country', 'latitude', 'longitude', 'created_at', 'updated_at']

class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = ['id', 'city', 'temperature', 'description', 'humidity', 'wind_speed', 'icon', 'created_at']

class WeatherSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherSearch
        fields = ['id', 'city', 'created_at'] 