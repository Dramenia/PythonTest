#!/bin/bash

set -e

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Run the Django server
exec "$@"
