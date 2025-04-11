from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}, {self.country}"

class WeatherData(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='weather_data')
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=200)
    humidity = models.IntegerField()
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2)
    icon = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Weather for {self.city.name} at {self.created_at}"

class WeatherSearch(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='searches')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Search for {self.city.name} at {self.created_at}"
