#!/bin/sh
set -e

# Migrations va boshqa konfiguratsiyalar
python manage.py migrate --noinput

# Crontabni o'rnatish
python manage.py crontab add

# Cron xizmatini ishga tushirish
cron -f &

# Gunicorn bilan ishlash
exec gunicorn core.wsgi:application --bind 0.0.0.0:8001 --workers 3
