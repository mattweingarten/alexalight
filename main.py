import logging
import requests
from flask import Flask, render_template, redirect
from flask_ask import Ask, statement, question, session
from flask_redis import FlaskRedis
from tasks import off, new_w
from bulb import power_on, power_off
from brightness import kelvin, brightness
from weather import sunrise_sunset
from flask.ext.dotenv import DotEnv


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
def options(option):
    if option == "automated":
        new_w.delay()
        msg = render_template('option') #call light function
        return statement(msg)

    elif option =="off":
        off.delay()
        power_off()
        return statement("Lights off")
    elif option =="sunrise":
        power_on(0.25,3000,55,0.8)
        return statement("Sunrise mode activated")


if __name__ == '__main__':
    app.run(debug=True)
