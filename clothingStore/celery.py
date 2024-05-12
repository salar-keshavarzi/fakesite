import os
from celery import Celery
from celery.schedules import crontab

BROKER_URL = 'redis://localhost:6379/0'
BROKER_URL2 = 'redis://localhost:63790'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothingStore.settings')
app = Celery('djangoOTP', broker=BROKER_URL)
app.conf.beat_schedule = {
    'db_backup_scheduler': {
        'task': 'clothingStore.tasks.backup_database',
        'schedule': crontab(minute='0', hour='3'),
    },
}
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
