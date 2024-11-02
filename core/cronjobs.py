"""
The cron-jobs module
"""

CRON_TASKS = [
    ('*/55 * * * *', 'apps.common.management.jobs.pg_dump')
]
