from flask import Flask, Response
import logging
from weather_service import WeatherService
from tile_generator import TileGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
weather_service = WeatherService()
tile_generator = TileGenerator()

@app.route('/')
def index():
    return '''<html>
<head>
    <title>Weather Map Tile Server</title>
</head>
<body>
    <h1>Weather Map Tile Server</h1>
    <p>Access tiles at: /tiles/{z}/{x}/{y}.svg</p>
    <p>Example: <a href="/tiles/10/512/512.svg">/tiles/10/512/512.svg</a></p>
</body>
</html>'''

@app.route('/tiles/<int:z>/<int:x>/<int:y>.svg')
def get_tile(z, x, y):
    try:
        lat, lon = tile_generator.tile_to_coordinates(x, y, z)
        logger.info(f"Tile request: z={z}, x={x}, y={y} -> lat={lat:.2f}, lon={lon:.2f}")
        
        weather_data = weather_service.get_weather(lat, lon)
        svg_content = tile_generator.generate_svg_tile(weather_data)
        
        return Response(svg_content, mimetype='image/svg+xml')
        
    except Exception as e:
        logger.error(f"Error generating tile: {e}")
        empty_svg = tile_generator._empty_tile()
        return Response(empty_svg, mimetype='image/svg+xml')

@app.errorhandler(404)
def not_found(e):
    return "Not found", 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {e}")
    return "Internal server error", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8112, debug=False)