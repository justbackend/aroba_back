"""
The cron-jobs module
"""

CRON_TASKS = [
    ('*/60 * * * *', 'apps.common.management.jobs.pg_dump')
]
