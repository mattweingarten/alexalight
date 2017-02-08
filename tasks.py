from celery.task import task
from celery import Celery
from celery.schedules import crontab
from celery.bin import worker
from weather import sunrise_sunset
from brightness import kelvin, brightness
from bulb import power_on,power_off

app = Celery('tasks', broker='redis://localhost:6379/0')

app.conf.timezone = 'Europe/London'

app.conf.update(worker_pool_restarts=True)

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.lights',
        'schedule': 420.0
    },
}

@app.task
def lights():
    sun = sunrise_sunset()
    b = brightness(sun['sunrise'],sun['sunset'],1)
    k = kelvin(sun['sunrise'],sun['sunset'],1)
    print b
    print k
    power_on(b,k)
    return

@app.task
def new_w():
    argv = ['worker','--loglevel=DEBUG','-B', '--hostname=worker2@dbc']
    app.worker_main(argv)
    return

@app.task
def off():
    app.control.broadcast('shutdown',destination=['worker2@dbc'])
    power_off()
