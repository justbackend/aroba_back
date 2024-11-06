#!/bin/bash
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

python manage.py crontab add

service cron start

exec gunicorn core.wsgi:application --bind 0.0.0.0:8001 --workers 4 --preload


