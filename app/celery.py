import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'b2bit.settings')

app = Celery('b2bit')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
