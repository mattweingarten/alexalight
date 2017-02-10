from celery import Celery
from tasks import app
from bulb import power_on, power_off
from celery.task.schedules import crontab
import time



@app.task
def set_alarm_time(hour, minute, day):
        app.conf.beat_schedule['light'].update({'schedule': crontab(hour=hour,minute=minute,day_of_week=day), 'task': 'alarm.alarm_mode'})
        return


@app.task
def alarm_mode():
    counter = 1
    while counter < 30:
        counter += 1
        power_on(1.0,6500,200,0,0.01)
        time.sleep(0.5)
        power_off(1)
    app.control.broadcast('shutdown',destination=['worker2@dbc'])
    power_off(1)
    return
