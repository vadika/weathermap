import math
import logging

logger = logging.getLogger(__name__)

class TileGenerator:
    def __init__(self):
        self.tile_size = 256
        
    def tile_to_coordinates(self, x, y, z):
        n = 2.0 ** z
        lon = x / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
        lat = math.degrees(lat_rad)
        return lat, lon
    
    def get_weather_icon(self, weather):
        icons = {
            'clear': '☀️',
            'clouds': '☁️',
            'rain': '🌧️',
            'drizzle': '🌦️',
            'thunderstorm': '⛈️',
            'snow': '❄️',
            'mist': '🌫️',
            'fog': '🌫️',
            'haze': '🌫️'
        }
        return icons.get(weather, '❓')
    
    def create_wind_arrow(self, direction):
        return f'<g transform="translate(55, 8) rotate({direction} 0 0)"><path d="M 0,-12 L -4,-4 L 0,-6 L 4,-4 Z" fill="black" stroke="black" stroke-width="1"/></g>'
    
    def generate_svg_tile(self, weather_data):
        if not weather_data:
            return self._empty_tile()
        
        temperature = weather_data['temperature']
        weather = weather_data['weather']
        wind_direction = weather_data['wind_direction']
        
        svg_content = f'''<svg width="{self.tile_size}" height="{self.tile_size}" xmlns="http://www.w3.org/2000/svg">
    <rect width="{self.tile_size}" height="{self.tile_size}" fill="transparent"/>
    <g transform="translate(10, 10)">
        <text x="20" y="15" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold">{temperature}°C</text>
        <text x="20" y="32" text-anchor="middle" font-family="Arial" font-size="16">{self.get_weather_icon(weather)}</text>
        {self.create_wind_arrow(wind_direction)}
    </g>
</svg>'''
        
        return svg_content
    
    def _empty_tile(self):
        return f'''<svg width="{self.tile_size}" height="{self.tile_size}" xmlns="http://www.w3.org/2000/svg">
    <rect width="{self.tile_size}" height="{self.tile_size}" fill="transparent"/>
</svg>'''