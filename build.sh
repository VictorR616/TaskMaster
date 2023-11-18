#!/usr/bin/env bash
# exit on error
set -o errexit

# Install or update pipenv
pip install --upgrade pipenv

# Activate the virtual environment
pipenv install --dev
pipenv shell

# Install dependencies
pipenv install --ignore-pipfile

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input
