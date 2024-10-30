#!/bin/sh
set -e



python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Agar gunicorn bn run qilsez
exec gunicorn core.wsgi:application --bind 0.0.0.0:8001

# Agar gunicorn ishlatmasez
#exec python manage.py runserver 0.0.0.0:8000
