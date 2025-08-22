#!/bin/sh
# start.sh

# echo "Applying database migrations..."
# python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Django server on port 8000..."
python manage.py runserver 0.0.0.0:8000
