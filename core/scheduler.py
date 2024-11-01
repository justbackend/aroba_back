from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: call_command('pg_dump_db'), 'interval', minutes=1)
    scheduler.start()
