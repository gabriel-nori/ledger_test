# Use an official Python base image
FROM python:3.10-alpine

RUN mkdir /backend

# Set the working directory in the container
WORKDIR /backend

# Copy the application code to the container
COPY ./backend/ ./

# Install necessary system dependencies
RUN apk add --no-cache build-base libpq libpq-dev

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Creates the static files to run admin and other internal applications
RUN python3 manage.py collectstatic --noinput

# Expose the default Django port
EXPOSE 8000

# To enable the application to auto start, we need this command to be set on the docker file
# I'm removing it from here and this is going to be passed in two distinct steps.
# The first one is to migrate the database and the second one to start the app.

# Here's the command to start the aplication:
# CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]

# Here's the command to migrate the database:
# CMD ["python", "manage. py", "migrate"]