import os
import re
from django.core.exceptions import ImproperlyConfigured

def get_api_key():
    """
    Get the OpenWeather API key from environment variables.
    Raises ImproperlyConfigured if the API key is not set or invalid.
    """
    api_key = os.getenv('OPENWEATHER_API_KEY')
    
    if not api_key:
        raise ImproperlyConfigured(
            "OpenWeather API key not found. Please set OPENWEATHER_API_KEY in your .env file."
        )
    
    # Validate API key format (OpenWeather API keys are 32 characters long)
    if not re.match(r'^[a-zA-Z0-9]{32}$', api_key):
        raise ImproperlyConfigured(
            "Invalid OpenWeather API key format. API key should be 32 characters long."
        )
    
    return api_key

def mask_api_key(api_key):
    """
    Mask the API key for logging purposes.
    Returns first 4 and last 4 characters with asterisks in between.
    """
    if not api_key or len(api_key) < 8:
        return "****"
    return f"{api_key[:4]}****{api_key[-4:]}" 