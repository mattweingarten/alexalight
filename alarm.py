from celery import Celery
from tasks import app
from bulb import power_on, power_off
from celery.task.schedules import crontab
import time

# app.conf.beat_schedule = {
#     'alarm': {
#         'task': 'alarm.alarm_mode',
#         'schedule': 1000000000000.0
#     },
#     'light': {
#         'task': 'tasks.lights',
#         'schedule': 300.0
#         }
# }
#

# @app.on_after_configure.connect
# def setup_alarm(sender, **kwargs):
#     sender.add_periodic_tasks(1000000, alarm_mode(),name='alarm')

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
