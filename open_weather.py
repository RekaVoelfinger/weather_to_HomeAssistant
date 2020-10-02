import requests
import json
import configparser
from datetime import datetime


def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api_key']


def get_weather(api_key, lattitude, longitude):
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lattitude}&lon={longitude}&units=metric&appid={api_key}"
    r = requests.get(url) # 'requests.models.Response' type
    return r.json() # returns 'dict' type


# for anlysis write the response to file
def write_to_file(file_name, response):
    with open(file_name, "w") as write_file:
        write_file.write(str(response))

# TODO elaborate the result of will_it_rain function
def will_it_rain(data_list, time_of_query): # call it in main with data_all_hours
    rainy_hours = {}
    count = 0
    for n in data_list:
        if data_list[n]['pop'] != '0':
            rainy_hours[str(int(time_of_query) + count)] = data_list[n]['pop']
    return rainy_hours



# Weidach coordinates (lat,lon): (48.45, 9.89)
def main():
    api_key = get_api_key()
    forecast = get_weather(api_key, "48.45", "9.89")
    data_all_hours = forecast['hourly'] # list type
    # print(f"data from hourly: {data_all_hours}")
    # print(data_all_hours[:11]) # forecast for the next 12 hour
    date_of_query = datetime.utcfromtimestamp(data_all_hours[0]['dt'] + forecast['timezone_offset']).strftime('%Y-%m-%d')
    time_of_query = datetime.utcfromtimestamp(data_all_hours[0]['dt'] + forecast['timezone_offset']).strftime('%H:%M')
    print(f"date_of_query: {date_of_query}") # TODO these prints belong to debug and log file
    print(f"time_of_query: {time_of_query}")
    print(f"Chance of rain: {100 * data_all_hours[1]['pop']}%")
    print(f"Temperature: {data_all_hours[1]['temp']}")
    print(f"Time: {datetime.utcfromtimestamp(data_all_hours[1]['dt']).strftime('%H:%M')}")

if __name__ == '__main__':
    main()