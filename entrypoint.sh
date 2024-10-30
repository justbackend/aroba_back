#!/bin/sh
set -e

python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Agar gunicorn bn run qilsez
# exec gunicorn project_name.wsgi:application --bind 0.0.0.0:8000

# Agar gunicorn ishlatmasez
exec python manage.py runserver 0.0.0.0:8000
