#!/bin/bash
set -e

python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='a').exists():
    User.objects.create_superuser('a', 'a', first_name='Ahmad', last_name='Abdurahimov')
EOF

/home/aroba-back/venv/bin/gunicorn -c gunicorn.py core.wsgi:application &
/home/aroba-back/venv/bin/daphne -b 0.0.0.0 -p 8002 core.asgi:application &

wait
