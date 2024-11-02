"""
The cron-jobs module
"""

CRON_TASKS = [
    ('*/1 * * * *', 'django.core.management.call_command', ['pg_dump_db'], '>> /tmp/pg_dump_job.log')
]
