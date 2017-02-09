from celery import Celery
from tasks import app


app.conf.beat_schedule = {
    'light': {
        'task': 'tasks.lights',
        'schedule': 300.0
    }
}


@app.task
def custom_automated(sunrise,sunset):
    app.conf.beat_schedule['light'].update({'args': (sunrise,sunset)})
    return
