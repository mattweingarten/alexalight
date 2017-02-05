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

from datetime import timedelta






app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


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
        api_key = "DARK SKY API KEY"
        lat = 37.773972
        lng = -122.431297
        forecast = forecastio.load_forecast(api_key, lat, lng)
        today = forecast.daily().data[0]
        sunrise = today.sunriseTime - timedelta(hours = 8 )
        sunset = today.sunsetTime - timedelta(hours = 8 )
        print sunrise
        print sunset

        b = round(brightness(sunrise,sunset,2),2)
        k = math.floor(kelvin(sunrise,sunset,2))
        power_on(b,k)

        msg = render_template('option',kelvin= k, bright = b) #call light function
        return statement(msg)

    elif option =="off":
        power_off()
        return statement("Lights off")

# while session.attributes['automated'] == True
#     POST LIGHTURL

# @app.route(LIGHTURL, method=['POST'])
#     now = datetime.now()

# @ask.intent("BrightnessIntent")



def kelvin(sunrise, sunset, int_length):
  x = amount_of_delta(sunrise,int_length) * delta_between_intervals(sunrise,sunset,int_length) - 1
  print x
  return kelvin_function(x)

def brightness(sunrise, sunset, int_length):
  x = amount_of_delta(sunrise,int_length) * delta_between_intervals(sunrise,sunset,int_length) - 1
  return brightness_function(x)



#private

def delta_between_intervals(sunrise, sunset, int_length):
  length_in_minutes = (sunset.hour - sunrise.hour) * 60 +  sunset.minute -  sunrise.minute
  max_int_count = length_in_minutes/int_length
  return 2.0/max_int_count

def amount_of_delta(sunrise,int_length):
  now = datetime.datetime.now()
  length_in_minutes = (now.hour - sunrise.hour) * 60 +  now.minute - sunrise.minute
  amount_of_intervals = length_in_minutes/int_length
  return amount_of_intervals


def brightness_function(x):
    brightness = -(x**4) + 1
    return brightness

def kelvin_function(x):
    kelvin = ((-0.69*(x**2)) + 1)* 6500
    return kelvin




token = "c2074e5b2a2df2ea1dda84e97d13944a97b2a80fd90ccae3c48c4d12c4c20c4c"

# response = requests.get('https://api.lifx.com/v1/lights/all', auth=(token, ''))
#
# print(response.content)
# print "******************"
#
headers = {
    "Authorization": "Bearer %s" % token,
}
#
# response_2 = requests.get('https://api.lifx.com/v1/lights/all', headers=headers)
#
# print(response_2.content)
# print "$$$$$$$$$$$$$$$$$"

def power_on(brightness, kelvin):
    payload = {
      "states": [
        {
            "selector" : "all",
            "hue": 200,
            "brightness": 0.1,
            "kelvin": kelvin
        }
      ],
      "defaults": {
        "power": "on",
        "saturation": 0,
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
	"power": "on",
	"saturation": 0,
	"duration": 2.0
	}
	}
	response = requests.put('https://api.lifx.com/v1/lights/states', data=json.dumps(payload), headers=headers)
	print(response.content)


if __name__ == '__main__':
    app.run(debug=True)
