from django.core.management import call_command


def pg_dump():
    call_command('pg_dump_db')
