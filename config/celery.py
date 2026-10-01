import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("email_assistant")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
