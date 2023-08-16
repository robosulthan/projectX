# django_celery/celery.py

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iksaan.settings")
app = Celery("iksaan")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
