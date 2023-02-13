import requests
import json

URL = 'http://colormind.io'


def get_color(model='default', input_list=None):
    url = URL + '/api/'
    data = {}
    if input_list is not None:
        data['input'] = input_list
    data['model'] = model
    try:
        response = requests.post(url, data=json.dumps(data), timeout=10)
        r = response.json()
    except requests.exceptions.RequestException as e:
        r = {'error': 'RequestException: ' + str(e)}
    return r


if __name__ == '__main__':
    print(get_color())
    lst = ["N", [88, 129, 111], [249, 247, 242], "N", "N"]
    print(get_color(input_list=lst))
