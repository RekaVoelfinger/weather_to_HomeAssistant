import requests

# Parameters see on: https://openweathermap.org/api/one-call-api
#  Blaustein-Wiedach geographic coordinates lat=48.445653, lon=9.887470

# response_all_info = requests. get('http://api.openweathermap.org/data/2.5/onecall?lat=48.45&lon=9.89&units=metric&appid=6ec4e9ae0169e18bdf68974e631274cc')
response = requests. get('http://api.openweathermap.org/data/2.5/weather?lat=48.45&lon=9.89&units=metric&appid=6ec4e9ae0169e18bdf68974e631274cc')
print(response.json())
print(response)