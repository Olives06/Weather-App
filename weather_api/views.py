import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

api_key = '5aa4346a08b00eae21856e2d7ba6a1a1'  # Replace with your key

@csrf_exempt
def get_weather(request):
    city = request.GET.get('city')
    if not city:
        return JsonResponse({'error': 'City not provided'}, status=400)

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return JsonResponse({'error': 'City not found'}, status=404)

    result = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed'],
        'icon': data['weather'][0]['icon']
    }
    return JsonResponse(result)


@csrf_exempt
def get_forecast(request):
    city = request.GET.get('city')
    if not city:
        return JsonResponse({'error': 'City not provided'}, status=400)

    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return JsonResponse({'error': 'City not found'}, status=404)

    forecast_list = data['list'][:6]  # First 6 entries (approx next 18 hrs)
    formatted = []

    for item in forecast_list:
        formatted.append({
            'dt_txt': item['dt_txt'],
            'main': {'temp': item['main']['temp']},
            'weather': [{
                'description': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon']
            }]
        })

    return JsonResponse({'forecast': formatted})
