# Weather Map Tile Server - Development Context

## Project Overview
A Python Flask application that serves weather information as map tiles in both SVG and PNG formats. The tiles display current weather data from OpenWeatherMap API.

## Key Features
- **Dual format support**: 
  - SVG tiles at `/tiles/{z}/{x}/{y}.svg` (vector format)
  - PNG tiles at `/tiles/{z}/{x}/{y}.png` (raster format)
- **Weather data displayed**:
  - Temperature in Celsius
  - Weather icon (emoji)
  - Wind direction indicator (arrow in SVG, triangle in PNG)
- **Caching**: 10-minute TTL cache for weather data to reduce API calls
- **Coordinate rounding**: Rounds to 2 decimal places for caching efficiency

## Technical Stack
- **Backend**: Flask (Python 3.11)
- **Image Processing**: Pillow for PNG generation, CairoSVG for SVG conversion
- **Caching**: cachetools with TTL cache
- **Containerization**: Docker with multi-stage build
- **Production**: Docker Compose with Nginx reverse proxy

## File Structure
- `app.py` - Main Flask application with routes
- `weather_service.py` - OpenWeatherMap API integration with caching
- `tile_generator.py` - SVG and PNG tile generation logic
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container configuration with system dependencies
- `docker-compose.yml` - Development deployment
- `docker-compose.prod.yml` - Production deployment with Nginx
- `nginx.conf` - Nginx configuration with caching and rate limiting

## Recent Changes
1. **PNG Support Added**: Direct PNG generation using Pillow with thin fonts and triangle wind indicators
2. **Production Setup**: Nginx reverse proxy on port 8112 with caching and rate limiting
3. **Docker Compose Update**: Updated to use `docker compose` (new syntax) instead of `docker-compose`
4. **Port Configuration**: Fixed port conflict - weathermap service exposes port internally, Nginx binds to host port 8112

## Environment Configuration
- Requires `OPENWEATHERMAP_API_KEY` in `.env` file
- Production uses `.env.production` file
- Port 8112 for both development and production

## Testing
- `test_map.html` - Leaflet map with SVG tiles
- `test_map_png.html` - Leaflet map with format switcher (SVG/PNG)

## Deployment Commands
```bash
# Development
docker build -t weathermap .
docker run -p 8112:8112 --env-file .env weathermap

# Production
./deploy.sh
# or
docker compose -f docker-compose.prod.yml up -d
```

## Known Issues Resolved
- Environment variable propagation in production fixed by removing redundant interpolation
- Port conflicts resolved by having weathermap service only expose port internally
- PNG fonts changed from bold to regular for cleaner appearance

## API Endpoints
- `/` - Home page with usage instructions
- `/tiles/{z}/{x}/{y}.svg` - Vector weather tiles
- `/tiles/{z}/{x}/{y}.png` - Raster weather tiles

## Future Considerations
- The server supports both SVG to PNG conversion via CairoSVG and direct PNG generation via Pillow
- Currently using direct PNG generation for better control over styling
- Weather icons use emoji which may render differently across systems