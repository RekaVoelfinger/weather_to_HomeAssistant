import logging
import api_helper, chart
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

# Return a dictionery with the predicted time and probability of rain in the next 12 hours
def will_it_rain(data_list, start_time, field): # call it in main with data_all_hours_ow, time_to_int(time_of_query_ow)
    rainy_hours = {}
    logging.debug(f"start_time: {start_time}")
    for h in range(12): # Range should be 1..12
        logging.debug(f"h: {h} : pop: {data_list[h][field]}")
        if data_list[h][field] > 0 and data_list[h][field] <= 1:
            rainy_hours[str(start_time + h)] = round(float(data_list[h][field])*100)
        else:
            rainy_hours[str(start_time + h)] = data_list[h][field]
    return rainy_hours

# Convert time string from time_of_query to integer.
def time_to_int(time_str):
    return int(time_str[:2])

# TODO Rainy hours to merge and/or pass to HomeAssistant
def main():

    logging.basicConfig(level=logging.WARNING)

    # OpenWeatherMap
    logging.info("\nOpenWeatherMap started...")

    logging.info("Getting config data...")
    url_ow = api_helper.get_config("openweathermap", "url")
    logging.debug(f"url: {url_ow}")

    logging.info("Getting weather data for Weidach (lat=48.45&lon=9.89)...")
    forecast_ow = get_weather(url_ow) # returns a dict {hourly: [ {1st hour...},{2nd hour...},..]}
    data_all_hours_ow = forecast_ow['hourly'] # list type
    logging.debug(f"Weather for the next 12 hour{data_all_hours_ow[:11]}") # forecast for the next 12 hour

    logging.info("Getting date and time...")
    logging.debug(f"Time: {data_all_hours_ow[0]['dt']}")
    date_of_query_ow = datetime.utcfromtimestamp(data_all_hours_ow[0]['dt'] + forecast_ow['timezone_offset']).strftime('%Y-%m-%d')
    time_of_query_ow = datetime.utcfromtimestamp(data_all_hours_ow[0]['dt'] + forecast_ow['timezone_offset']).strftime('%H:%M')
    logging.debug(f"date_of_query_ow: {date_of_query_ow}")
    logging.debug(f"time_of_query_ow: {time_of_query_ow}")

    logging.debug(f"Chance of rain now: {100 * data_all_hours_ow[0]['pop']}%")
    logging.info(f"Temperature: {data_all_hours_ow[1]['temp']}")
    rainy_hours_ow = will_it_rain(data_all_hours_ow, time_to_int(time_of_query_ow), 'pop')
    logging.info(f"Rainy hours: {rainy_hours_ow}")
    logging.info("OpenWeatherMap finished.")

    # AccuWeather
    logging.info("\nAccuWeather started...")

    logging.info("Getting config data...")
    url_acw = api_helper.get_config("accuweather", "url")
    logging.debug(f"url: {url_acw}")

    logging.info("Getting weather data for Weidach (location key=986294, lat=48.45, lon=9.89)...")
    forecast_acw = get_weather(url_acw)
    logging.debug(f"Weather data: {forecast_acw}")

    logging.info("Getting date and time...")
    logging.debug(f"Time: {forecast_acw[0]['EpochDateTime']}")
    time_of_query_acw = datetime.utcfromtimestamp(forecast_acw[0]['EpochDateTime']).strftime('%H:%M')
    logging.info(f"time_of_query: {time_of_query_acw}")
    rainy_hours_acw = will_it_rain(forecast_acw, time_to_int(time_of_query_acw), 'RainProbability')
    logging.info(f"Rainy hours: {rainy_hours_acw}")
    logging.info("AccuWeather finished.")

    # TODO Error handling
    ''' 
    # WeatherBit
    # It does not work anymore "Your API key does not allow access to this endpoint."
    
    logging.info("\nWeatherBit started...")

    logging.info("Getting config data...")
    url_wbit = api_helper.get_config("weatherbit", "url")
    logging.debug(f"url: {url_wbit}")

    logging.info("Getting weather data for Weidach ( lat=48.45, lon=9.89)...")
    forecast_wbit = get_weather(url_wbit) # returns a dict {data: [ {1st hour...},{2nd hour...},..]}
    logging.debug(f"forecast_wbit: {forecast_wbit}")
    data_forecast_wbit = forecast_wbit['data']
    logging.debug(f"Weather data: {data_forecast_wbit}")

    logging.info(f"Getting time...")
    logging.debug(f"Time: {data_forecast_wbit[0]['ts']}")
    time_of_query_wbit = datetime.utcfromtimestamp(data_forecast_wbit[0]['ts']).strftime('%H:%M')
    logging.info(f"time_of_query: {time_of_query_wbit}")
    rainy_hours_wbit = will_it_rain(data_forecast_wbit, time_to_int(time_of_query_wbit), 'pop')
    logging.info(f"Rainy hours: {rainy_hours_wbit}")
    logging.info("WeatherBit finished.")
    '''

    #print(f"Rainy hours:\n{rainy_hours_ow}\n{rainy_hours_acw}\n{rainy_hours_wbit}")
    chart.draw_chart(["blue", "orange", "green"], ["OpenWeatherMap", "AccuWeather", "WeatherBit"], rainy_hours_ow, rainy_hours_acw)
    # TODO run this script in HomeAssistant
    # TODO Copy file to 192.168.1.152/local

if __name__ == '__main__':
    main()