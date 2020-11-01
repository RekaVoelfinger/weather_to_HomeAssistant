import configparser
import requests

# Get api_key or url
def get_config(service_name, config_data):
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config[service_name][config_data]

# AccuWeather needs to get Location Key for given (latitude,longitude)
# Weidach coordinates are (lat,lon): (48.45, 9.89)
def get_location_key(api_key, lat, lon):
    url = f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={api_key}&details=true&q=" + lat +"," + lon
    response_location_key = requests.get(url)
    location = response_location_key.json()
    print(f"Location Key for {location['LocalizedName']}: {location['Key']}")
    return location['Key']


