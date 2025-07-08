# Weather Map Tile Server

A Python application that provides weather information as transparent SVG map tiles via HTTP.

## Features

- Serves z-x-y map tiles as transparent SVG images
- Displays current weather information in the top-left corner of each tile:
  - Temperature in Celsius
  - Weather icon (cloudy, sunny, rain, snow, etc.)
  - Wind direction arrow
- Fetches weather data from OpenWeatherMap API
- Caches weather data by rounded coordinates (2 decimal places) to reduce API calls
- Runs on port 8112

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and add your OpenWeatherMap API key:
   ```
   cp .env.example .env
   ```
3. Edit `.env` and set your API key:
   ```
   OPENWEATHERMAP_API_KEY=your_actual_api_key_here
   ```

## Running with Docker

Build the Docker image:
```bash
docker build -t weathermap .
```

Run the container:
```bash
docker run -p 8112:8112 --env-file .env weathermap
```

## Running locally

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the application:
```bash
python app.py
```

## Usage

Access tiles at:
```
http://localhost:8112/tiles/{z}/{x}/{y}.svg
```

Example:
```
http://localhost:8112/tiles/10/512/512.svg
```

## API Endpoints

- `/` - Home page with basic information
- `/tiles/{z}/{x}/{y}.svg` - Get weather tile for specific coordinates

## Production Deployment

### Using Docker Compose

1. Copy the production environment file:
   ```bash
   cp .env.production.example .env.production
   ```

2. Edit `.env.production` with your production API key

3. Deploy using the provided script:
   ```bash
   ./deploy.sh
   ```

Or manually:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Production Features

- **Nginx reverse proxy** with caching and rate limiting
- **Health checks** for automatic container recovery
- **Resource limits** to prevent memory/CPU issues
- **Persistent logging** with rotation
- **CORS headers** for cross-origin requests
- **10-minute cache** for weather tiles
- **Rate limiting** at 10 requests/second per IP

### SSL/HTTPS Setup

1. Place your SSL certificates in `./ssl/` directory
2. Uncomment the HTTPS server block in `nginx.conf`
3. Update the server_name with your domain
4. Redeploy the services