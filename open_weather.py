import requests
import json
import configparser

'''
OpenWeather
Parameters see on: https://openweathermap.org/api/one-call-api
Blaustein-Wiedach geographic coordinates lat=48.445653, lon=9.887470

To get access to current weather, minute forecast for 1 hour, hourly forecast for 48 hours, daily forecast for 7 days and government weather alerts.
For hourly and daily forecast only add parameter 'exclude=current,minutely'
response_all_info = requests. get('http://api.openweathermap.org/data/2.5/onecall?lat=48.45&lon=9.89&units=metric&appid=6ec4e9ae0169e18bdf68974e631274cc')
Eg.
Response current weather in Weidach
# response = requests. get('http://api.openweathermap.org/data/2.5/weather?lat=48.45&lon=9.89&units=metric&appid=6ec4e9ae0169e18bdf68974e631274cc')
'''

def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api_key']


def get_weather(api_key, lattitude, longitude):
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lattitude}&lon={longitude}&units=metric&appid={api_key}"
    r = requests.get(url)
    return r.json()


# for anlysis write the response to file
def write_to_file(file_name, response):
    with open(file_name, "w") as write_file:
        write_file.write(str(response))

# Weidach coordinates (lat,lon): (48.45, 9.89)
def main():
    api_key = get_api_key()
    forecast = get_weather(api_key, "48.45", "9.89")
   # write_to_file("response.json", forecast)
    print(forecast['hourly']['weather'])


if __name__ == '__main__':
    main()