import threading

import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

scheduler = None
scheduler_lock = threading.Lock()


def start_scheduler():
    pass
    # global scheduler
    # with scheduler_lock:
    #     if scheduler is None:
    #         scheduler = BackgroundScheduler()
    #         scheduler.add_job(lambda: call_command('pg_dump_db'), 'interval', minutes=33)
    #         scheduler.start()
