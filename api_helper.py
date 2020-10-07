import configparser

def get_api_key(service_name):
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config[service_name]['api_key']


