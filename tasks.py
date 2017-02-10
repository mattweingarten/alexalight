from celery.task import task
from celery import Celery
from celery.schedules import crontab
from celery.bin import worker
from weather import sunrise_sunset
from brightness import kelvin, brightness
from bulb import power_on,power_off
from flask_ask import session
from celery.signals import celeryd_init
from helper import from_string_to_time
from random import randint

app = Celery('tasks', broker='redis://localhost:6379/0')

app.conf.timezone = 'US/Pacific-New'

app.conf.update(worker_pool_restarts=True)
from automated import custom_automated
from alarm import set_alarm_time


@app.task
def new_w():
    argv = ['celery','-A','automated','--loglevel=DEBUG','-B', '--hostname=worker2@dbc']
    app.worker_main(argv)
    return


@app.task
def new_alarm():
    argv = ['celery','-A','alarm','--loglevel=DEBUG','-B', '--hostname=worker2@dbc']
    app.worker_main(argv)
    return


@app.task
def off():
    app.control.broadcast('shutdown',destination=['worker2@dbc'])
    power_off()

@app.task
def lights(sunrise=None,sunset=None):
    print app.conf.beat_schedule['light']
    if (sunrise == None and sunset == None ):
        sun = sunrise_sunset()
        b = brightness(sun['sunrise'],sun['sunset'],1)*0.8
        k = kelvin(sun['sunrise'],sun['sunset'],1)
        power_on(b,k)
    else:
        sunrise =  from_string_to_time(sunrise.encode('ascii','ignore'))
        sunset =  from_string_to_time(sunset.encode('ascii','ignore'))
        b = brightness(sunrise,sunset,1)*0.9
        k = kelvin(sunrise,sunset,1)
        power_on(b,k)
    return

@app.task
def party():
    power_on(1,4500,randint(0,350),1,0.5)


@app.task
def party_mode():
        print app.conf.beat_schedule['light']
        app.conf.beat_schedule['light'].update({'schedule': 3, 'task': 'tasks.party'})
        return
