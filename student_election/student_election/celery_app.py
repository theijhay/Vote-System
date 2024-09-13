import os
import sys
from celery import Celery

"""Add the parent directory to sys.path"""
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

"""Set the default Django settings module for Celery"""
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_election.settings')

app = Celery('student_election')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
