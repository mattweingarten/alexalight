from celery import Celery
from tasks import app


app.conf.beat_schedule = {
    'lights': {
        'task': 'tasks.lights',
        'schedule': 30.0
    }
}


@app.task
def custom_automated(sunrise,sunset):
    print app.conf.beat_schedule['lights']
    app.conf.beat_schedule['lights'].update({'args': (sunrise,sunset)})  
    print app.conf.beat_schedule['lights']
    return
