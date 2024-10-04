#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e


cd /var/www/project/sitslot
# Pull the latest code
echo "Pulling the latest code..."
git pull origin main

# Take down the existing containers (if running)
echo "Stopping any running containers..."
docker-compose down

# Build and start containers in detached mode
echo "Building and starting the containers..."
docker-compose up -d --build

# Wait for services to be up (Optional: Add a health check if necessary)
sleep 10  # Adjust this wait time if necessary

# Run database migrations (if needed)
echo "Running database migrations..."
docker-compose exec web python manage.py migrate

# Restart services (if needed)
echo "Restarting services..."
docker-compose restart

# Optional: Show logs if needed (useful for debugging)
echo "Showing Docker logs for debugging purposes..."
docker-compose logs -f
