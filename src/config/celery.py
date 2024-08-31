from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django의 settings 모듈을 Celery의 설정으로 사용
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# Django의 settings.py에서 정의된 모든 Celery 관련 설정을 가져오기
app.config_from_object("django.conf:settings", namespace="CELERY")

# Django에서 자동으로 task를 검색하여 자동 로드
app.autodiscover_tasks()
