import logging

import requests

import math

from random import randint

from flask import Flask, render_template, redirect

from flask_ask import Ask, statement, question, session

import time

import json

import forecastio

import datetime

from flask_redis import FlaskRedis

from datetime import timedelta

from datetime import datetime

from celery.task.control import revoke


from tasks import off, on, new_w

import os

app = Flask(__name__)

redis_store = FlaskRedis(app)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)



# app.config.update(
#     CELERY_BROKER_URL='redis://localhost:6379',
#     CELERY_RESULT_BACKEND='redis://localhost:6379'
# )
#
# def make_celery(app):
#     celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
#                     broker=app.config['CELERY_BROKER_URL'])
#     celery.conf.update(app.config)
#     TaskBase = celery.Task
#     class ContextTask(TaskBase):
#         abstract = True
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return TaskBase.__call__(self, *args, **kwargs)
#     celery.Task = ContextTask
#     return celery
#
# celery = make_celery(app)
#
#
# @celery.task()
# def add(x,y):
#     return x + y

@ask.launch

def light_options():
    msg = render_template('intro')
    return question(msg).reprompt("Do you need help?")


@ask.intent("HelpIntent")

def help_options():
    msg = render_template('help', options= ["automated", "on", "off", "wake"])
    return question(msg)


@ask.intent("StopIntent")
def stop():
    return statement("")


@ask.intent("OptionIntent")
def options(option):
    if option == "automated":
        new_w.delay()
        msg = render_template('option',kelvin= k, bright = b) #call light function
        return statement(msg)

    elif option =="off":
        off.delay()
        power_off()
        return statement("Lights off")
    elif option =="sunrise":
        power_on(0.25,3000,55,0.8)
        return statement("Sunrise mode activated")

















token = "c2074e5b2a2df2ea1dda84e97d13944a97b2a80fd90ccae3c48c4d12c4c20c4c"

headers = {
    "Authorization": "Bearer %s" % token,
}


def power_on(brightness, kelvin, hue=200, saturation=1.0):
    payload = {
      "states": [
        {
            "selector" : "all",
            "hue": hue,
            "brightness": brightness,
            "kelvin": kelvin
        }
      ],
      "defaults": {
        "power": "on",
        "saturation": saturation,
        "duration": 5.0

    	}
    }

    response = requests.put('https://api.lifx.com/v1/lights/states', data=json.dumps(payload), headers=headers)
    print(response.content)



def power_off():
	payload = {
	"states": [
	{
	"selector" : "all",
	"power": "off"
	}
	],
	"defaults": {
	"power": "off",
	"saturation": 0,
	"duration": 2.0
	}
	}
	response = requests.put('https://api.lifx.com/v1/lights/states', data=json.dumps(payload), headers=headers)
	print(response.content)


if __name__ == '__main__':
    app.run(debug=True)
