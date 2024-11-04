#!/bin/bash
set -e

# Django migrations
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Crontab qo'shish
python manage.py crontab add

# Cron xizmatini to'g'ridan-to'g'ri sessiyada ishga tushirish
#cron -f &
service cron start

# Asosiy dasturlarni ishga tushirish
exec gunicorn core.wsgi:application --bind 0.0.0.0:8001 --workers 4 --preload


