from celery import Celery
from tasks import app



app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.lights',
        'schedule': 420.0
    },
}


@app.task
def lights():
    sun = sunrise_sunset()
    b = brightness(sun['sunrise'],sun['sunset'],1)*0.9
    k = kelvin(sun['sunrise'],sun['sunset'],1)
    power_on(b,k)
    return
