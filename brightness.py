from datetime import datetime
from datetime import timedelta
from datetime import time
import math


def kelvin(sunrise, sunset, int_length):
  x = amount_of_delta(sunrise,sunset,int_length) * delta_between_intervals(sunrise,sunset,int_length) - 1

  return math.floor(kelvin_function(x))

def brightness(sunrise, sunset, int_length):
  x = amount_of_delta(sunrise,sunset,int_length) * delta_between_intervals(sunrise,sunset,int_length) - 1
  bright = round(brightness_function(x),2)
  if bright < 0:
    return 0
  else:
    return bright



#private

def delta_between_intervals(sunrise, sunset, int_length):

  if sunrise.hour <= sunset.hour:
      length_in_minutes = (sunset.hour - sunrise.hour) * 60 +  sunset.minute -  sunrise.minute
  else:
      length_in_minutes = (sunset.hour - sunrise.hour + 24) * 60 +  sunset.minute -  sunrise.minute
  max_int_count = length_in_minutes/int_length
  return 2.0/max_int_count

def amount_of_delta(sunrise,sunset,int_length):
  now = datetime.now()
  if (sunrise.hour <= sunset.hour and sunset.hour >= now.hour):
      length_in_minutes = (sunset.hour - now.hour) * 60 +  (sunset.minute -  now.minute)
  else:
      length_in_minutes = (sunset.hour - now.hour + 24) * 60 +  sunset.minute -  now.minute

  amount_of_intervals = length_in_minutes/int_length
  return amount_of_intervals


def brightness_function(x):
    brightness = -(x**4) + 1
    return brightness

def kelvin_function(x):
    kelvin = ((-0.69*(x**2)) + 1)* 6500
    return kelvin
