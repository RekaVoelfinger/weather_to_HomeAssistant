import api_helper
import requests
import json
from datetime import datetime

# TODO get_wether could be general with args?
# Get weather data from OpenWeatherMap
def get_weather_ow(api_key, lattitude, longitude, url):
    #url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lattitude}&lon={longitude}&units=metric&appid={api_key}"
    r = requests.get(url) # 'requests.models.Response' type
    return r.json() # returns 'dict' type

'''
def get_weather_ow(api_key, lattitude, longitude):
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lattitude}&lon={longitude}&units=metric&appid={api_key}"
    r = requests.get(url) # 'requests.models.Response' type
    return r.json() # returns 'dict' type
'''

# Get weather data from AccuWeather
def get_weather_acw(api_key, location_key, url):
    #url = f"http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{location_key}?apikey={api_key}&details=true&metric=true"
    r = requests.get(url)  # 'requests.models.Response' type TODO watch 401 error code 
    return r.json()  # returns 'dict' type


# for anlysis write the response to file
def write_to_file(file_name, response):
    with open(file_name, "w") as write_file:
        write_file.write(str(response))

# Return a dictionery with the predicted time and probability of rain
def will_it_rain(data_list, start_time, hours): # call it in main with data_all_hours_ow, time_to_int(time_of_query_ow)
    rainy_hours = {}
    print(f"start_time: {start_time}")
    for h in range(hours):
        print(f"h: {h} : pop: {data_list[h]['pop']}")
        if data_list[h]['pop'] != 0:
            rainy_hours[str(start_time + h)] = data_list[h]['pop']
    return rainy_hours

# TODO create a general function from will_it_rain
def will_it_rain_acw(data_list, start_time, hours): # call it in main with forecast_acw, time_to_int(time_of_query_ow)
    rainy_hours = {}
    print(f"start_time: {start_time}")
    for h in range(hours):
        print(f"h: {h} : pop: {data_list[h]['RainProbability']}")
        if data_list[h]['RainProbability'] != 0:
            rainy_hours[str(start_time + h)] = data_list[h]['RainProbability']
    return rainy_hours

# Convert time string from time_of_query to integer.
def time_to_int(time_str):
    return int(time_str[:2])

# Weidach coordinates (lat,lon): (48.45, 9.89)
def main():

    # OpenWeatherMap
    api_key_ow = api_helper.get_config("openweathermap","api_key") #TODO !!{'cod': 401, 'message': 'Invalid API key. Please see http://openweathermap.org/faq#error401 for more info.'}
    url_ow = api_helper.get_config("openweathermap", "url")
    forecast_ow = get_weather_ow(api_key_ow, "48.45", "9.89", url_ow)
    data_all_hours_ow = forecast_ow['hourly'] # list type
    # print(f"data from hourly: {data_all_hours_ow}")
    # print(data_all_hours_ow[:11]) # forecast for the next 12 hour
    date_of_query_ow = datetime.utcfromtimestamp(data_all_hours_ow[0]['dt'] + forecast_ow['timezone_offset']).strftime('%Y-%m-%d')
    time_of_query_ow = datetime.utcfromtimestamp(data_all_hours_ow[0]['dt'] + forecast_ow['timezone_offset']).strftime('%H:%M')
    print(f"date_of_query_ow: {date_of_query_ow}") # TODO these prints belong to debug and log file
    print(f"time_of_query_ow: {time_of_query_ow}")
    print(f"Chance of rain: {100 * data_all_hours_ow[1]['pop']}%")
    print(f"Temperature: {data_all_hours_ow[1]['temp']}")
    print(f"Rainy hours: {will_it_rain(data_all_hours_ow, time_to_int(time_of_query_ow), 12)}")


    # AccuWeather
    api_key_acw = api_helper.get_config("accuweather", "api_key")
    url_acw = api_helper.get_config("accuweather", "url")
    # location_key = "986294"  # Weidach
    location_key = api_helper.get_location_key(api_key_acw, "48.45", "9.89")
    forecast_acw = get_weather_acw(api_key_acw, location_key, url_acw)
    time_of_query_acw = datetime.utcfromtimestamp(forecast_acw[0]['EpochDateTime'] + 7200).strftime('%H:%M') # TODO time can be common with OpenWeather
    print(f"time_of_query: {time_of_query_acw}")
    print(f"Rainy hours: {will_it_rain_acw(forecast_acw, time_to_int(time_of_query_acw), 12)}") #TODO Clarify the time by the different services

if __name__ == '__main__':
    main()