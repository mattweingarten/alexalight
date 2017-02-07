from celery.task import task
from celery import Celery
from celery.schedules import crontab
from celery.bin import worker




app = Celery('tasks', broker='redis://localhost:6379/0')

app.conf.timezone = 'Europe/London'

app.conf.update(worker_pool_restarts=True)

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.lights',
        'schedule': 5.0
    },
}


@app.task
def lights():
    print "changes lights"
    return


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

@app.task
def off():
    app.control.broadcast('shutdown',destination=['worker2@dbc'])
