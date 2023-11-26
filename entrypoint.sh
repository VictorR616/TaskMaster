#!/bin/sh
echo 'Running collecstatic...'
python manage.py collectstatic --no-input --settings=taskmaster.settings.production

echo 'Running migrations...'
python manage.py migrate --settings=taskmaster.settings.production

echo 'Running server...'
gunicorn --env DJANGO_SETTINGS_MODULE=taskmaster.settings.production taskmaster.wsgi:application --bind 0.0.0.0:8000