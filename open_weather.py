import api_helper
import requests
import json
from datetime import datetime


def get_weather(api_key, lattitude, longitude):
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lattitude}&lon={longitude}&units=metric&appid={api_key}"
    r = requests.get(url) # 'requests.models.Response' type
    return r.json() # returns 'dict' type


# for anlysis write the response to file
def write_to_file(file_name, response):
    with open(file_name, "w") as write_file:
        write_file.write(str(response))

# Return a dictionery with the predicted time and probability of rain
def will_it_rain(data_list, start_time, hours): # call it in main with data_all_hours, time_to_int(time_of_query)
    rainy_hours = {}
    print(f"start_time: {start_time}") # TODO why start_time = 1 ???
    for h in range(hours):
        print(f"h: {h} : pop: {data_list[h]['pop']}")
        if data_list[h]['pop'] != 0:
            rainy_hours[str(start_time + h)] = data_list[h]['pop']
    return rainy_hours

# Convert time string from time_of_query to integer
def time_to_int(time_str):
    return int(time_str[:2])

# Weidach coordinates (lat,lon): (48.45, 9.89)
def main():
    api_key_ow = api_helper.get_api_key('openweathermap')
    forecast = get_weather(api_key_ow, "48.45", "9.89")
    data_all_hours = forecast['hourly'] # list type
    # print(f"data from hourly: {data_all_hours}")
    # print(data_all_hours[:11]) # forecast for the next 12 hour
    date_of_query = datetime.utcfromtimestamp(data_all_hours[0]['dt'] + forecast['timezone_offset']).strftime('%Y-%m-%d')
    time_of_query = datetime.utcfromtimestamp(data_all_hours[0]['dt'] + forecast['timezone_offset']).strftime('%H:%M')
    print(f"date_of_query: {date_of_query}") # TODO these prints belong to debug and log file
    print(f"time_of_query: {time_of_query}")
    print(f"Chance of rain: {100 * data_all_hours[1]['pop']}%")
    print(f"Temperature: {data_all_hours[1]['temp']}")
    print(f"Rainy hours: {will_it_rain(data_all_hours, time_to_int(time_of_query), 12)}")


if __name__ == '__main__':
    main()