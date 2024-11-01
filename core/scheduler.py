from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
import threading

scheduler = None
scheduler_lock = threading.Lock()


def start_scheduler():
    global scheduler
    with scheduler_lock:
        if scheduler is None:
            scheduler = BackgroundScheduler()
            scheduler.add_job(lambda: call_command('pg_dump_db'), 'interval', seconds=10)
            scheduler.start()
