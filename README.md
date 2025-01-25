# Django Ledger APP

This is a simple ledger application, allowing to create new financial accounts, transactions and keep track of the balance

## Features

- **Pre-configured Settings**: Organized and modular settings for development, testing, and production.
- **Reusable Structure**: A scalable app layout for adding new features easily.
- **Built-in Tools**:
  - Debugging with `django-debug-toolbar`.
  - Static and media file management.
  - Logging configuration for better monitoring.
- **Test-Ready**: Includes testing tools and sample test cases.
- **Docker Support**: Containerized environment for easy setup.

## Prerequisites

- Python 3.8+
- Django 4.x
- Docker (optional, for containerized development)
- PostgreSQL

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd higlobe_dev_test
```

### 2. Set Up a Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Project

1. Copy the `.env.example` file to `.env` and update the variables as needed:
   ```bash
   cp .env.example .env
   ```
2. Update database settings and secrets in the `.env` file.

### 5. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000/`.

## Project Structure

```plaintext
backend/
    ├── manage.py
    ├── config/        # Main app folder
    │   ├── settings    # Organized settings
    │   ├── urls.py      # Project URL configurations
    │   ├── wsgi.py      # WSGI application
    ├── api/        # Main api folder
    ├── apps/        # Main app folder. All created apps goes in this directory
    ├── .env.example     # Sample environment variables
    ├── requirements.txt # Project dependencies
README.md        # Project documentation
```

## Deployment

### Using Docker

1. Build the Docker image:
   ```bash
   docker build -t higlobe_dev_test .
   ```
2. Run the container:
   ```bash
   docker run -d -p 8000:8000 --env-file .env higlobe_dev_test
   ```

### Manual Deployment

1. Set up a production server (e.g., Gunicorn, Nginx).
2. Apply production settings from `settings/production.py`.
3. Use a WSGI server to serve the application.

## Testing

Run tests with:

```bash
python manage.py test
```
