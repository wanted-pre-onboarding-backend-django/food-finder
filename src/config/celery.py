import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)
app.autodiscover_tasks()
app.conf.timezone = 'Asia/Seoul'

app.conf.beat_schedule = {
    # TODO: run_full_pipeline task 설정
    # "test-schedule": {
    #     "task": "config.tasks.run_full_pipeline",
    #     'schedule': timedelta(minutes=2),
    # }
}
