# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /sitslot

# Copy the current directory contents into the container at /sitslot
COPY . /sitslot

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt


RUN python manage.py migrate

# Collect static files (only for production)
RUN python manage.py collectstatic --noinput

# Expose port 8000 to the world outside this container
EXPOSE 8000

# Set environment variables (optional)
# ENV DJANGO_SETTINGS_MODULE sitslot.settings.production

# Add health check to ensure the service is healthy
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl --fail http://localhost:8000 || exit 1

# Copy entrypoint.sh to container and set as entrypoint
# COPY entrypoint.sh /sitslot/entrypoint.sh
# ENTRYPOINT ["/sitslot/entrypoint.sh"]

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
