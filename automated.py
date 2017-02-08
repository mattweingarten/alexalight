from celery import Celery
from tasks import app



app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.lights',
        'schedule': 420.0
    },
}
