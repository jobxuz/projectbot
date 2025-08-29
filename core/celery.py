import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Notification system va boshqa tasklar uchun schedule
from core.celery_schedule import CELERY_BEAT_SCHEDULE
app.conf.beat_schedule = CELERY_BEAT_SCHEDULE
app.conf.timezone = 'Asia/Tashkent'
