"""
Command-line app to query the current weather
and forecast for the next 24 hours at 3-hour intervals.
"""
from datetime import datetime
import requests

API_KEY = ''

city = input('Enter city name: ')

loc_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={API_KEY}'

loc_response = requests.get(loc_url, timeout=10)
loc_data = loc_response.json()


# convert temperature from Kelvin to Celsius
def convert_temp(temp_k):
    """"
    Converts temperature from Kelvin to Celsius"""
    temp_c = temp_k - 273.15
    return temp_c


if loc_response.status_code == 200:

    # get latitude and longitude
    lat = loc_data[0]["lat"]
    lon = loc_data[0]["lon"]

    # get URLs for the weather and the forecast
    weather_url = (f'https://api.openweathermap.org/data/2.5/weather?'
                   f'lat={lat}&lon={lon}&appid={API_KEY}')
    forecast_url = (f'https://api.openweathermap.org/data/2.5/forecast?'
                    f'lat={lat}&lon={lon}&appid={API_KEY}')

    # set weather response from URL to JSON
    weather_response = requests.get(weather_url, timeout=10)
    weather_data = weather_response.json()

    # set forecast response from URL to JSON
    forecast_response = requests.get(forecast_url, timeout=10)
    forecast_data = forecast_response.json()

    if weather_response.status_code == 200:

        description = weather_data["weather"][0]["description"]
        temp_kelvin = weather_data["main"]["temp"]
        feels_like = weather_data["main"]["feels_like"]
        temp_max = weather_data["main"]["temp_max"]
        temp_min = weather_data["main"]["temp_min"]
        humidity = weather_data["main"]["humidity"]
        sunrise = weather_data["sys"]["sunrise"]
        sunset = weather_data["sys"]["sunset"]

        # convert timestamp to readable date
        sunrise_ts = int(sunrise)
        sunrise_time = datetime.utcfromtimestamp(sunrise_ts).strftime("%H:%M:%S")
        sunset_ts = int(sunset)
        sunset_time = datetime.utcfromtimestamp(sunset_ts).strftime("%H:%M:%S")

        # convert temperatures from Kelvin to Celsius
        temp_celsius = convert_temp(temp_kelvin)
        feels_like_celsius = convert_temp(feels_like)
        max_celsius = convert_temp(temp_max)
        min_celsius = convert_temp(temp_min)

        # get current date and time
        current_datetime = datetime.now()
        current_date = current_datetime.strftime('%d/%m/%Y')
        current_time = current_datetime.strftime("%H:%M:%S")

        # print data
        print(current_date, current_time)
        print(f'Weather: {description}')
        print(f'Temperature: {temp_celsius:.1f}°C')
        print(f'Feels like: {feels_like_celsius:.1f}°C')
        print(f'Max: {max_celsius:.1f}°C, min: {min_celsius:.1f}°C')
        print(f'Humidity: {humidity}%')
        print(f'Sunrise at {sunrise_time}')
        print(f'Sunset at {sunset_time}')

    else:
        print('Error fetching weather data')

else:
    print('Error fetching location data')
