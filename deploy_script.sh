#!/bin/bash



# Pull the latest code
git pull origin main

# Install dependencies
docker-compose down
docker-compose up -d --build

# Run database migrations (if needed)
docker-compose exec web python manage.py migrate

# Restart services
docker-compose restart
