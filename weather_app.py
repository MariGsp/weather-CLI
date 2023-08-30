import requests

api_key = 0

city = input('Enter city name: ')


loc_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}'


loc_response = requests.get(loc_url)
loc_data = loc_response.json()


if loc_response.status_code == 200:
    
    lat = loc_data[0]["lat"]
    lon = loc_data[0]["lon"]

    weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'

    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    if weather_response.status_code == 200:

        weather = weather_data["weather"][0]["main"]
        description = weather_data["weather"][0]["description"]
        temp_kelvin = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]

        temp_celsius = temp_kelvin - 273.15

        print(f'{weather}: {description}')
        print(f'Temp: {temp_celsius:.2f}°C')
        print(f'Humidity: {humidity}%')
    else:
        print('Error fetching weather data')

else:
    print('Error fetching location data')
