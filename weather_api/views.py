from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import WeatherData, City, WeatherSearch
from .serializers import WeatherDataSerializer, CitySerializer, WeatherSearchSerializer
from .utils import get_api_key, mask_api_key
import requests
from datetime import datetime
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class WeatherViewSet(viewsets.ModelViewSet):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer

    @action(detail=False, methods=['post'])
    def fetch_weather(self, request):
        city = request.data.get('city', '')
        if not city:
            return Response(
                {'error': 'City name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            api_key = get_api_key()
            logger.info(f"Fetching weather for city: {city} using API key: {mask_api_key(api_key)}")
            
            # Fetch weather data from OpenWeather API
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                # Save weather data to database
                weather_data = WeatherData.objects.create(
                    city=city,
                    temperature=data['main']['temp'],
                    humidity=data['main']['humidity'],
                    description=data['weather'][0]['description'],
                    wind_speed=data['wind']['speed']
                )

                # Update or create city record
                City.objects.update_or_create(
                    name=city,
                    defaults={
                        'country': data['sys']['country'],
                        'last_updated': datetime.now()
                    }
                )

                serializer = self.get_serializer(weather_data)
                return Response(serializer.data)
            else:
                error_message = data.get('message', 'Unknown error')
                logger.error(f"Weather API error for city {city}: {error_message}")
                return Response(
                    {'error': f'Could not fetch weather data: {error_message}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            logger.error(f"Error fetching weather data: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        city = request.query_params.get('city', None)
        if not city:
            return Response({'error': 'City parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get weather data from OpenWeatherMap API
            api_key = settings.OPENWEATHER_API_KEY
            if not api_key:
                return Response({'error': 'OpenWeatherMap API key is not configured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Get current weather
            current_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
            current_response = requests.get(current_url)
            
            if current_response.status_code != 200:
                return Response({'error': 'Failed to fetch weather data'}, status=current_response.status_code)

            current_data = current_response.json()

            # Get forecast data
            forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
            forecast_response = requests.get(forecast_url)
            
            if forecast_response.status_code != 200:
                return Response({'error': 'Failed to fetch forecast data'}, status=forecast_response.status_code)

            forecast_data = forecast_response.json()

            # Create or update city
            city_obj, created = City.objects.get_or_create(
                name=current_data['name'],
                defaults={
                    'country': current_data['sys']['country'],
                    'latitude': current_data['coord']['lat'],
                    'longitude': current_data['coord']['lon']
                }
            )

            # Create weather data
            weather_data = WeatherData.objects.create(
                city=city_obj,
                temperature=current_data['main']['temp'],
                description=current_data['weather'][0]['description'],
                humidity=current_data['main']['humidity'],
                wind_speed=current_data['wind']['speed'],
                icon=current_data['weather'][0]['icon']
            )

            # Log the search
            WeatherSearch.objects.create(city=city_obj)

            # Process forecast data
            forecast_list = []
            for item in forecast_data['list'][:8]:  # Get next 24 hours (3-hour intervals)
                forecast_list.append({
                    'dt_txt': item['dt_txt'],
                    'temp': item['main']['temp'],
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon'],
                    'humidity': item['main']['humidity'],
                    'wind_speed': item['wind']['speed']
                })

            # Return the data
            return Response({
                'city': CitySerializer(city_obj).data,
                'weather': WeatherDataSerializer(weather_data).data,
                'forecast': forecast_list
            })

        except Exception as e:
            logger.error(f"Error fetching weather data: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WeatherDataViewSet(viewsets.ModelViewSet):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer

class WeatherSearchViewSet(viewsets.ModelViewSet):
    queryset = WeatherSearch.objects.all()
    serializer_class = WeatherSearchSerializer
