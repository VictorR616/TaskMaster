#!/usr/bin/env bash
# exit on error
set -o errexit


pipenv install


# Run migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input
