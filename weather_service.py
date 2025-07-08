import os
import requests
from cachetools import TTLCache
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        if not self.api_key:
            raise ValueError("OPENWEATHERMAP_API_KEY environment variable is not set")
        
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.cache = TTLCache(maxsize=10000, ttl=600)  # Cache for 10 minutes
        
    def _round_coordinates(self, lat, lon):
        return round(lat, 2), round(lon, 2)
    
    def get_weather(self, lat, lon):
        lat_rounded, lon_rounded = self._round_coordinates(lat, lon)
        cache_key = f"{lat_rounded},{lon_rounded}"
        
        if cache_key in self.cache:
            logger.info(f"Cache hit for coordinates: {cache_key}")
            return self.cache[cache_key]
        
        try:
            params = {
                'lat': lat_rounded,
                'lon': lon_rounded,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            weather_data = {
                'temperature': round(data['main']['temp']),
                'weather': data['weather'][0]['main'].lower(),
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind']['deg']
            }
            
            self.cache[cache_key] = weather_data
            logger.info(f"Fetched weather for coordinates: {cache_key}")
            
            return weather_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather data: {e}")
            return None
        except KeyError as e:
            logger.error(f"Unexpected response format: {e}")
            return None