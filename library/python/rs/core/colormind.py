import requests
import json


def get_color():
    url = 'http://colormind.io/api/'
    data = {'model': 'default'}
    try:
        response = requests.post(url, data=json.dumps(data), timeout=10)
        r = response.json()
    except requests.exceptions.RequestException as e:
        r = {'error': 'RequestException: ' + str(e)}
    return r
