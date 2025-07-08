import math
import logging
from PIL import Image, ImageDraw, ImageFont
import io
import cairosvg

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
    
    def svg_to_png(self, svg_content):
        try:
            png_data = cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), 
                                       output_width=self.tile_size, 
                                       output_height=self.tile_size)
            return png_data
        except Exception as e:
            logger.error(f"Error converting SVG to PNG: {e}")
            return self._empty_png()
    
    def _empty_png(self):
        img = Image.new('RGBA', (self.tile_size, self.tile_size), (255, 255, 255, 0))
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        return buffer.getvalue()
    
    def generate_png_tile(self, weather_data):
        if not weather_data:
            return self._empty_png()
        
        # Create transparent PNG
        img = Image.new('RGBA', (self.tile_size, self.tile_size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw weather info
        temperature = weather_data['temperature']
        weather = weather_data['weather']
        wind_direction = weather_data['wind_direction']
        
        # Try to use a basic font
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
            icon_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        except:
            font = ImageFont.load_default()
            icon_font = font
        
        # Temperature text
        draw.text((20, 10), f"{temperature}°C", fill=(0, 0, 0, 255), font=font, anchor="mt")
        
        # Weather icon (using text emoji)
        icon = self.get_weather_icon(weather)
        draw.text((20, 25), icon, fill=(0, 0, 0, 255), font=icon_font, anchor="mt")
        
        # Wind arrow
        self._draw_wind_arrow(draw, 55, 8, wind_direction)
        
        # Convert to bytes
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        return buffer.getvalue()
    
    def _draw_wind_arrow(self, draw, x, y, direction):
        # Convert direction to radians
        angle = math.radians(direction)
        
        # Arrow points
        length = 12
        head_length = 4
        
        # Calculate end point
        end_x = x + length * math.sin(angle)
        end_y = y - length * math.cos(angle)
        
        # Calculate arrow head points
        head_angle1 = angle - math.pi / 6
        head_angle2 = angle + math.pi / 6
        
        head_x1 = end_x - head_length * math.sin(head_angle1)
        head_y1 = end_y + head_length * math.cos(head_angle1)
        
        head_x2 = end_x - head_length * math.sin(head_angle2)
        head_y2 = end_y + head_length * math.cos(head_angle2)
        
        # Draw arrow
        draw.line([(x, y), (end_x, end_y)], fill=(0, 0, 0, 255), width=2)
        draw.polygon([(end_x, end_y), (head_x1, head_y1), (head_x2, head_y2)], 
                     fill=(0, 0, 0, 255))