from datetime import datetime, timedelta
import math


def kelvin(sunrise, sunset, int_length):
  x = amount_of_delta(sunrise,int_length) * delta_between_intervals(sunrise,sunset,int_length) - 1

  return math.floor(kelvin_function(x))

def brightness(sunrise, sunset, int_length):
  x = amount_of_delta(sunrise,int_length) * delta_between_intervals(sunrise,sunset,int_length) - 1
  bright = round(brightness_function(x),2)
  if bright < 0:
    return 0
  else:
    return bright



#private

def delta_between_intervals(sunrise, sunset, int_length):
  length_in_minutes = (sunset.hour - sunrise.hour) * 60 +  sunset.minute -  sunrise.minute
  max_int_count = length_in_minutes/int_length
  return 2.0/max_int_count

def amount_of_delta(sunrise,int_length):
  now = datetime.now()
  length_in_minutes = (now.hour - sunrise.hour) * 60 +  now.minute - sunrise.minute
  amount_of_intervals = length_in_minutes/int_length
  return amount_of_intervals


def brightness_function(x):
    brightness = -(x**4) + 1
    return brightness

def kelvin_function(x):
    kelvin = ((-0.69*(x**2)) + 1)* 6500
    return kelvin
