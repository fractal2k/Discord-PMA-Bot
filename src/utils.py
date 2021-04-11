import json
import requests


def get_quote():
    url = 'https://zenquotes.io/api/random'
    response = json.loads(requests.get(url).text)
    return response[0]['q'] + ' - ' + response[0]['a']
