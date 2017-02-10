import forecastio
from datetime import timedelta
from flask.ext.dotenv import DotEnv

def sunrise_sunset():
    api_key ="f7ec6ca728a76e5aa63b2cce4fda43b0"
    lat = 37.773972
    lng = -122.431297
    forecast = forecastio.load_forecast(api_key, lat, lng)
    today = forecast.daily().data[0]
    sunrise = today.sunriseTime - timedelta(hours = 8 )
    sunset = today.sunsetTime - timedelta(hours = 8 )
    return {'sunrise': sunrise, 'sunset': sunset}
