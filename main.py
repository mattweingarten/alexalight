import logging
import requests
from flask import Flask, render_template, redirect
from flask_ask import Ask, statement, question, session
from flask_redis import FlaskRedis
from tasks import off, new_w, lights, new_alarm
from automated import custom_automated
from bulb import power_on, power_off
from brightness import kelvin, brightness
from weather import sunrise_sunset
from flask.ext.dotenv import DotEnv
import datetime
import time
from alarm import set_alarm_time
from helper import from_string_to_time, day_of_week
app = Flask(__name__)
env = DotEnv(app)
redis_store = FlaskRedis(app)

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
def options(option,sunrise,sunset,day):
    if option == "automated":
        if (sunrise == None and sunset == None):
            new_w.delay()
            lights.delay()
        else:
            sunrise = from_string_to_time(sunrise)
            sunset = from_string_to_time(sunset)

            ##I dont know why but it only works with many updates
            custom_automated.delay(sunrise, sunset)
            custom_automated.delay(sunrise, sunset)
            custom_automated.delay(sunrise, sunset)
            custom_automated.delay(sunrise, sunset)
            custom_automated.delay(sunrise, sunset)
            lights.delay(sunrise,sunset)
            new_w.delay()
            custom_automated.delay(sunrise, sunset)
            custom_automated.delay(sunrise, sunset)
            custom_automated.delay(sunrise, sunset)
            custom_automated.delay(sunrise, sunset)
            custom_automated.delay(sunrise, sunset)
            custom_automated.delay(sunrise, sunset)

        msg = render_template('option') #call light function
        return statement(msg)

    elif option == "alarm":
        s = from_string_to_time(sunrise)
        h = s.hour
        m = s.minute
        d = day_of_week(day)
        set_alarm_time.delay(h,m,d)
        set_alarm_time.delay(h,m,d)
        set_alarm_time.delay(h,m,d)
        set_alarm_time.delay(h,m,d)
        new_alarm.delay()
        set_alarm_time.delay(h,m,d)
        set_alarm_time.delay(h,m,d)
        set_alarm_time.delay(h,m,d)
        set_alarm_time.delay(h,m,d)
        return statement("Alarm mode!")
    elif option =="off":
        off.delay()
        time.sleep(3)
        power_off()
        return statement("Lights off")

    elif option =="on":
        power_on(0.75 ,2700 ,200, .2, 2.0)#This brightness will light up the room
        return statement("Lights on")

    elif option =="sunrise":#Sunrise is good tp gp
        power_on(0.55, 2500, 50, 0.8, 20.0)
        return statement("Sunrise mode activated")

    elif option =="sunset":
        power_on(0.45, 2500, 50, 0.8, 20.0)#Made a little brighter than sunrise but good to go
        return statement("Sunset mode activated")

    elif option =="night":
        power_on(0.05, 2100, 175, .90, 2.0)#Maybe this is the right blue or maybe more purple?
        return statement("Night mode activated")

    elif option =="party":
        power_on(.75, 2200, 300, 0.5, 2.0)#create a task to go through various colors
        return statement("Party mode activated")

    elif option =="romance":
        power_on(0.2, 1500, 300, 0.5, 2.0)#Pink? I think its not that bad
        return statement("Romance mode")




if __name__ == '__main__':
    app.run(debug=True)
