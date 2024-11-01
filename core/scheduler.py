import threading

import redis
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
from redis.exceptions import LockError

redis_client = redis.Redis(host='localhost', port=6379, db=0)

scheduler = None
scheduler_lock = threading.Lock()


def start_scheduler():
    global scheduler
    with scheduler_lock:
        if scheduler is None:
            scheduler = BackgroundScheduler()
            scheduler.add_job(lambda: call_command('pg_dump_db'), 'interval', minutes=33)
            scheduler.start()
