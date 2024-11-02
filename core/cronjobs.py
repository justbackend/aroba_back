"""
The cron-jobs module
"""

CRON_TASKS = [
    ('*/1 * * * *', 'apps.common.management.jobs.pg_dump')
]
