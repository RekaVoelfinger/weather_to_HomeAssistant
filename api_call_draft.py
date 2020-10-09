import requests

'''
OpenWeather
Parameters see on: https://openweathermap.org/api/one-call-api
Blaustein-Wiedach geographic coordinates lat=48.445653, lon=9.887470

To get access to current weather, minute forecast for 1 hour, hourly forecast for 48 hours, daily forecast for 7 days and government weather alerts.
For hourly and daily forecast only add parameter 'exclude=current,minutely'
response_all_info = requests. get('http://api.openweathermap.org/data/2.5/onecall?lat=48.45&lon=9.89&units=metric&appid=6ec4e9ae0169e18bdf68974e631274cc')
'''

# Response current weather in Weidach
# response = requests. get('http://api.openweathermap.org/data/2.5/weather?lat=48.45&lon=9.89&units=metric&appid=6ec4e9ae0169e18bdf68974e631274cc')

#Response hourly forecast in Weidach
# response_openw = requests. get('http://api.openweathermap.org/data/2.5/onecall?lat=48.45&lon=9.89&units=metric&exclude=current,minutely,daily&appid=6ec4e9ae0169e18bdf68974e631274cc')
# print(response_openw.json())

'''
AccuWeather
https://developer.accuweather.com/accuweather-forecast-api/apis
curl -X GET "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=a2Ak2hMxpoLv0KbGapaQwC4rUSYlmu5N&q=48.445653%2C9.887470&details=true"
Location key for Weidach: "Key": "986294"
'''

# Get Location Key for given (latitude,longitude)
def get_location_key(lat,lon):
    url = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=a2Ak2hMxpoLv0KbGapaQwC4rUSYlmu5N&details=true&q=" + lat +"," + lon
    response_location_key = requests.get(url)
    location = response_location_key.json()
    print(f"Location Key for {location['LocalizedName']}: {location['Key']}")
    return location['Key']

# get_location_key("48.445653", "9.887470")

# Response hourly forecast in Weidach
# response_accuw = requests.get("http://dataservice.accuweather.com/forecasts/v1/daily/1day/986294?apikey=a2Ak2hMxpoLv0KbGapaQwC4rUSYlmu5N&details=true&metric=true")
# print(response_accuw.json())


'''
WeatherBit
https://www.weatherbit.io/api
'''

response_wbit = requests.get("https://api.weatherbit.io/v2.0/forecast/hourly?key=4afa4e8e50d84ec587996b1a1ae60713&hours=48")
print(response_wbit.json())