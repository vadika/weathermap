#!/bin/bash

# Production deployment script

set -e

echo "🚀 Starting production deployment..."

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "❌ Error: .env.production file not found!"
    echo "Please copy .env.production.example to .env.production and configure it."
    exit 1
fi

# Check if API key is configured
if ! grep -q "OPENWEATHERMAP_API_KEY=." .env.production; then
    echo "❌ Error: OPENWEATHERMAP_API_KEY not configured in .env.production!"
    echo "Please edit .env.production and add your API key."
    exit 1
fi

echo "✅ Environment configuration verified"

# Pull latest changes (if using git)
# git pull origin main

# Build the image
echo "📦 Building Docker image..."
docker-compose -f docker-compose.prod.yml build

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down

# Start new containers
echo "🚀 Starting new containers..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for health check
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check container status
echo "📊 Container status:"
docker-compose -f docker-compose.prod.yml ps

# Show logs
echo "📝 Recent logs:"
docker-compose -f docker-compose.prod.yml logs --tail=20

echo "✅ Deployment complete!"
echo "🌐 Weather map service is available at:"
echo "   - HTTP: http://localhost"
echo "   - Direct: http://localhost:8112"

# Debug mode
if [ "$1" = "--debug" ]; then
    echo ""
    echo "🔍 Debug: Checking environment variables in container..."
    docker-compose -f docker-compose.prod.yml exec weathermap sh -c 'echo "API Key present: $(if [ -n "$OPENWEATHERMAP_API_KEY" ]; then echo "Yes"; else echo "No"; fi)"'
fi