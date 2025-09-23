# social_scheduler/celery.py

import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_scheduler.settings')

# Create a Celery application instance
app = Celery('social_scheduler')

# Load task configuration from Django settings.
# The configuration key is 'CELERY_' (e.g., CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps (like posting_agent/tasks.py)
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')