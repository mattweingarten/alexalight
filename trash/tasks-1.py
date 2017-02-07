from celery.task import task
from celery import Celery
from celery.schedules import crontab
from datetime import datetime
from time import time, sleep
from celery.task.control import revoke
from celery.task.control import inspect
import os
import requests
from random import randint
import json
from celery.bin import worker
import forecastio
from datetime import timedelta
import datetime




token = "c2074e5b2a2df2ea1dda84e97d13944a97b2a80fd90ccae3c48c4d12c4c20c4c"
# from werkzeug.contrib.cache import SimpleCache
headers = {
    "Authorization": "Bearer %s" % token,
}
# cache = SimpleCache()
app = Celery('tasks', broker='redis://localhost:6379/0')

app.conf.timezone = 'Europe/London'

app.conf.update(worker_pool_restarts=True)

@app.task
def lights():
    print "changes lights"


@app.task
def new_w():
    print "New workerforce!"
    argv = [
        'worker',
        '--loglevel=DEBUG',
        '-B',
        '--hostname=worker2@dbc'
    ]
    app.worker_main(argv)
    return
#
#


# @app.task
# def nothing():
#     return "nothing"
# @app.task
# def status(status):
#     def test(arg, status=status):
#         if status == True:
#             print(arg)
#     return test

#
@app.task
def off():
    app.control.broadcast('shutdown',destination=['worker2@dbc'])


# @app.task
# def on():
#     os.system('celery -A tasks worker -B')
#     return
#
# @app.task
# def delete():
#     i = inspect()
#     revoke(str(i.active()),terminate=True)
#     return
#
# @app.task
# def insp():
#     i = inspect()
#     return i.active()
#
# @app.task()
# def time():
#     while 1 == 1:
#
#         print(datetime.now())
#         sleep(5)
# #
# @app.task
# def automated(status):
#     if status == True:
#         app.conf.beat_schedule = {
#             'add-every-30-seconds': {
#                 'task': 'tasks.add',
#                 'schedule': 1.0,
#                 'args': (4,4)
#             },
#         }
#     else:
#         app.conf.beat_schedule = {
#             'add-every-30-seconds': {
#                 'task': 'task.nothing',
#                 'schedule': 1.0
#             },
#         }



# @app.task
# def current_task_id():
#     return app.current_task.request.id
# @app.task
# def off(i):
#     app.control.purge()

# # @app.task
# def time():
#     return(datetime.now())
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task       (10.0, test.s('hello'), name='add every 10')
#
#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(30.0, test.s('world'), expires=10)
#
#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         test.s('Happy Mondays!'),
#     )
