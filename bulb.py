import json
import requests
from flask.ext.dotenv import DotEnv

token = "token"

headers = {
    "Authorization": "Bearer %s" % token,
}

def power_on(brightness, kelvin, hue=200, saturation=0, duration=1.0):
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
      "duration": duration
      }
      }
    response = requests.put('https://api.lifx.com/v1/lights/states', data=json.dumps(payload), headers=headers)
    print(response.content)

def power_off(duration = 2.0):
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
	"duration": duration
	}
	}
	response = requests.put('https://api.lifx.com/v1/lights/states', data=json.dumps(payload), headers=headers)
	print(response.content)
