import os

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from utils import send_me

bot_token = settings.DUMP_BOT_TOKEN
chat_id = settings.DUMP_CHAT_ID


class Command(BaseCommand):
    help = 'Create a PostgreSQL dump of the database and send it via Telegram bot'
    URL = f'https://api.telegram.org/bot{bot_token}/sendDocument'
    FILE_PATH = 'dump.sql'

    def handle(self, *args, **kwargs):
        try:
            db_name = settings.DATABASES['default']['NAME']
            db_user = settings.DATABASES['default']['USER']
            db_password = settings.DATABASES['default']['PASSWORD']
            db_host = settings.DATABASES['default']['HOST']
            db_port = settings.DATABASES['default']['PORT']

            output_file = 'dump.sql'
            command = f'pg_dump -U {db_user} -h {db_host} -p {db_port} {db_name} > {self.FILE_PATH}'

            os.environ['PGPASSWORD'] = db_password

            try:
                os.system(command)
                self.stdout.write(self.style.SUCCESS(f'Successfully dumped the database to {output_file}'))

                self.send_to_telegram()
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
        except Exception as e:
            send_me(str(e))

    def send_to_telegram(self):
        now = timezone.now()
        caption = (
            f'New Dump File \n'
            f'created_at: {now.strftime("%d/%m/%Y %H:%M:%S")}'
        )

        with open(self.FILE_PATH, 'rb') as file:
            files = {'document': file}
            data = {'chat_id': chat_id, 'caption': caption}

            requests.post(self.URL, data=data, files=files)
