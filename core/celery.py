import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

celery =  Celery('core')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks() # this fun() tells django celery to automatically discover tasks func assigned in our project
