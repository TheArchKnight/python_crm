# django_celery/celery.py

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm_django.settings")
app = Celery("crm_celery")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
