from celery import shared_task
from django.core.management import call_command


@shared_task
def backup_database():
    # print('backup_database_called!!!')
    try:
        call_command('dbbackup')
    except:
        pass
