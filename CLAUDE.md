# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure

This is a Django project with machine learning focus:

- **ML/**: Main Django project directory
  - **ML/**: Django configuration package
    - `settings.py`: Django settings (uses SQLite database)
    - `urls.py`: URL routing configuration
    - `wsgi.py`: WSGI configuration
    - `asgi.py`: ASGI configuration
  - **model/**: Django application for ML models
    - `models.py`: Database models (currently empty)
    - `views.py`: View functions (currently empty)
    - `apps.py`: App configuration
  - `manage.py`: Django management commands
- **vrt/**: Python virtual environment (should be activated when working)

## Development Commands

### Virtual Environment
```bash
# Activate virtual environment (Windows)
vrt\Scripts\activate

# Activate virtual environment (Linux/Mac)
source vrt/bin/activate
```

### Django Commands
```bash
# Run development server
python ML/manage.py runserver

# Create migrations
python ML/manage.py makemigrations

# Apply migrations
python ML/manage.py migrate

# Create superuser
python ML/manage.py createsuperuser

# Run tests
python ML/manage.py test

# Collect static files
python ML/manage.py collectstatic
```

## Architecture Notes

- This is a fresh Django 5.2.4 project with minimal configuration
- Uses SQLite database (development only)
- The 'model' app is registered but not yet added to INSTALLED_APPS
- No custom models, views, or URLs have been implemented yet
- Secret key is using default Django insecure key (should be changed for production)

## Key Files

- `ML/ML/settings.py`: Contains project settings including database configuration
- `ML/manage.py`: Entry point for Django management commands
- `ML/model/`: Directory for ML-related Django app

## Working Directory

Always run Django commands from the project root directory (`/mnt/c/PYTHON DJANGO PROJECT/Machine_Learning/Model_0.0`).