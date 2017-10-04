import json
import urllib.request


class Weather:
    API_URL = 'http://api.wunderground.com/api/{key}/{req}/q/{state}/{city}.json'

    def __init__(self, api_key, city, state):
        self.api_key = api_key
        self.city = city.replace(' ', '_')
        self.state = state

    def get_conditions(self):
        url = self.API_URL.format(req='conditions', key=self.api_key, city=self.city, state=self.state)

        with urllib.request.urlopen(url) as request:
            data = json.loads(request.read().decode())

        return data
