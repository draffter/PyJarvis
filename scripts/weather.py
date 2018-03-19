# -*- coding: utf-8 -*-
from webcrawler import WebCrawler
import urllib
import json
from translator import ngettext


class Weather(object):

    def __init__(self, api_key, city, lang="pl", units="metric"):
        self.api_key = api_key
        self.city = city
        self.lang = lang
        self.units = units
        self.uri = "http://api.openweathermap.org/data/2.5/weather"
        self.speech_string = ""

    def get_one_day(self):
        params = {'q': self.city, 'appid': self.api_key, 'lang': self.lang, 'units': self.units}
        uri = self.uri + "?" + urllib.urlencode(params, True)
        print uri
        data = WebCrawler.get_data(uri)
        print(data)
        self.decode_json(data)
        return self.speech_string

    def decode_json(self, string_data):
        self.speech_string = _("weather.actual") + " "
        data = json.loads(string_data)
        if "weather" in data and isinstance(data["weather"], list) and "description" in data["weather"][0]:
            self.speech_string += data["weather"][0]["description"]
            self.speech_string += " "
        if "main" in data and "temp" in data["main"]:
            temp = data["main"]["temp"]
            self.speech_string += ngettext("%d weather.degree", "%d weather.degrees", temp) % temp
