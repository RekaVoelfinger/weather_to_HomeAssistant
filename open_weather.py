import logging
import api_helper
import requests
import json
from datetime import datetime


# Get weather data from OpenWeatherMap
def get_weather(url):
    r = requests.get(url) # 'requests.models.Response' type
    return r.json() # returns 'dict' type

# for anlysis write the response to file
def write_to_file(file_name, response):
    with open(file_name, "w") as write_file:
        write_file.write(str(response))

# Return a dictionery with the predicted time and probability of rain in the next 12 hours TODO can be hours global variable?
def will_it_rain(data_list, start_time, field): # call it in main with data_all_hours_ow, time_to_int(time_of_query_ow)
    rainy_hours = {}
    print(f"start_time: {start_time}")
    for h in range(12):
        print(f"h: {h} : pop: {data_list[h][field]}")
        if data_list[h][field] != 0:
            rainy_hours[str(start_time + h)] = data_list[h][field]
    return rainy_hours

# Convert time string from time_of_query to integer.
def time_to_int(time_str):
    return int(time_str[:2])


def main():

    logging.basicConfig(level=logging.INFO)

    # OpenWeatherMap
    logging.info("OpenWeatherMap started...")
    logging.info("Getting config data...")
    url_ow = api_helper.get_config("openweathermap", "url")
    logging.debug(f"url: {url_ow}")
    logging.info("Getting weather data for Weidach (lat=48.45&lon=9.89)...")
    forecast_ow = get_weather(url_ow)
    data_all_hours_ow = forecast_ow['hourly'] # list type
    logging.debug(f"Weather for the next 12 hour{data_all_hours_ow[:11]}") # forecast for the next 12 hour
    logging.info("Getting date and time...")
    logging.debug(f"Time: {data_all_hours_ow[0]['dt']}")
    date_of_query_ow = datetime.utcfromtimestamp(data_all_hours_ow[0]['dt'] + forecast_ow['timezone_offset']).strftime('%Y-%m-%d')
    time_of_query_ow = datetime.utcfromtimestamp(data_all_hours_ow[0]['dt'] + forecast_ow['timezone_offset']).strftime('%H:%M')
    logging.debug(f"date_of_query_ow: {date_of_query_ow}")
    logging.debug(f"time_of_query_ow: {time_of_query_ow}")
    logging.debug(f"Chance of rain now: {100 * data_all_hours_ow[1]['pop']}%")
    logging.info(f"Temperature: {data_all_hours_ow[1]['temp']}")
    logging.info(f"Rainy hours: {will_it_rain(data_all_hours_ow, time_to_int(time_of_query_ow), 'pop')}")
    logging.info("OpenWeatherMap finished.")

    # AccuWeather
    logging.info("AccuWeather started...")
    logging.info("Getting config data...")
    url_acw = api_helper.get_config("accuweather", "url")
    logging.debug(f"url: {url_acw}")
    logging.info("Getting weather data for Weidach (location key=986294, lat=48.45, lon=9.89)...")
    forecast_acw = get_weather(url_acw)
    logging.info("Getting date and time...")
    logging.debug(f"Time: {forecast_acw[0]['EpochDateTime']}")
    time_of_query_acw = datetime.utcfromtimestamp(forecast_acw[0]['EpochDateTime']).strftime('%H:%M') # TODO time can be common with OpenWeather?
    logging.info(f"time_of_query: {time_of_query_acw}")
    logging.info(f"Rainy hours: {will_it_rain(forecast_acw, time_to_int(time_of_query_acw), 'RainProbability')}") # TODO which is the first hour at the different services?
    logging.info("AccuWeather finished.")

    # WeatherBit TODO get the rainy hours from it
    logging.info("WeatherBit started...")
    logging.info("Getting config data...")
    url_wbit = api_helper.get_config("weatherbit", "url")
    logging.debug(f"url: {url_wbit}")
    logging.info("Getting weather data for Weidach ( lat=48.45, lon=9.89)...")
    forecast_wbit = get_weather(url_wbit)
    logging.info(f"{forecast_wbit}")
    logging.info("WeatherBit finished.")


if __name__ == '__main__':
    main()