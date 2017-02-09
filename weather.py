import forecastio
from datetime import timedelta
from flask.ext.dotenv import DotEnv

def sunrise_sunset():
    api_key ="darksky api key"
    lat = 37.773972
    lng = -122.431297
    forecast = forecastio.load_forecast(api_key, lat, lng)
    today = forecast.daily().data[0]
    sunrise = today.sunriseTime - timedelta(hours = 8 )
    sunset = today.sunsetTime - timedelta(hours = 8 )
    return {'sunrise': sunrise, 'sunset': sunset}
