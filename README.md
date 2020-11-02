# weather_to_HomeAssistant
Collect weather data from different webseites and make a card from it in HomeAssistant

SOURCES

OpenWeather
-----------
Parameters see on: https://openweathermap.org/api/one-call-api
Blaustein-Wiedach geographic coordinates lat=48.445653, lon=9.887470

To get access to current weather, minute forecast for 1 hour, hourly forecast for 48 hours, daily forecast for 7 days and government weather alerts.
For hourly and daily forecast only add parameter 'exclude=current,minutely'
response_all_info = requests. get('http://api.openweathermap.org/data/2.5/onecall?lat=48.45&lon=9.89&units=metric&appid=6ec4e9ae0169e18bdf68974e631274cc')
Eg.
Response current weather in Weidach
# response = requests. get('http://api.openweathermap.org/data/2.5/weather?lat=48.45&lon=9.89&units=metric&appid=6ec4e9ae0169e18bdf68974e631274cc')

AccuWeather
------------
Location key for Weidach: 986294
url=http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/986294?apikey=a2Ak2hMxpoLv0KbGapaQwC4rUSYlmu5N&details=true&metric=true

WeatherBit
------------

Parameters see on: https://www.weatherbit.io/api/weather-forecast-120-hour
