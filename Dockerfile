# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /sitslot

# Copy the current directory contents into the container at /sitslot
COPY . /sitslot

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt


RUN python manage.py collectstatic --noinput
# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable (optional, based on your app)
# ENV ENV_VAR_NAME value

# Run the application (update this to your actual command)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]