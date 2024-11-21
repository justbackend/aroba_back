#!/bin/bash
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

python manage.py crontab add

service cron start

python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='a').exists():
    User.objects.create_superuser('a', 'a', first_name='Ahmad', last_name='Abdurahimov')
EOF

exec gunicorn core.wsgi:application --bind 0.0.0.0:8001 --workers 4 &

exec daphne -u /tmp/daphne.sock core.asgi:application --bind 0.0.0.0 --port 8002

