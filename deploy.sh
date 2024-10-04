#!/bin/bash

set -e  # Exit on error

cd /var/www/project/sitslot || { echo "Directory not found"; exit 1; }

echo "Pulling the latest code..."
git pull origin main

echo "Stopping any running containers..."
docker-compose down || echo "No containers to stop."

echo "Building and starting the containers..."
docker-compose up -d --build

echo "Waiting for services to be up..."
sleep 10  # Adjust as needed

echo "Running database migrations..."
docker-compose exec web python manage.py migrate

echo "Restarting services..."
docker-compose restart

echo "Showing Docker logs for debugging..."
docker-compose logs -f
