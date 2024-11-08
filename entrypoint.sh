#!/bin/bash
set -e


./wait-for-it.sh aroba_db:5432 --timeout=30 --strict -- echo "Database aroba_db is up"

python manage.py migrate --noinput
python manage.py collectstatic --noinput

python manage.py crontab add

service cron start

python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='a').exists():
    User.objects.create_superuser('a', 'a')
EOF

exec gunicorn core.wsgi:application --bind 0.0.0.0:8001 --workers 4


