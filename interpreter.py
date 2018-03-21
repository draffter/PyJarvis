# -*- coding: utf-8 -*-
import snowboydecoder
import speech_recognition as sr
from speaker import Speaker
from scripts.weather import Weather
from scripts.kodi import Kodi
from scripts.calendar import Calendar
from translator import ngettext


class Interpreter(object):
    def __init__(self, config):
        self.config = config
        self.weather = Weather(
            self.config.get_string("WEATHER", "api_key"),
            self.config.get_string("WEATHER", "city"),
            self.config.get_string("WEATHER", "lang"),
            self.config.get_string("WEATHER", "units")
        )
        self.kodi = Kodi(port=self.config.get_string("KODI", "port"))
        self.recognizer = sr.Recognizer()
        self.calendar = Calendar()

    def calibrate(self, callback):
        Speaker.talk(_("jarvis.initialize.start"))
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, 2)
        self.recognizer.dynamic_energy_threshold = True
        Speaker.talk(_("jarvis.initialize.end"))
        callback()

    def listen(self):
        with sr.Microphone() as source:
            print("Say something!")
            audio = self.recognizer.listen(source)
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
        try:
            data = self.recognizer.recognize_google(audio,
                                                    language=self.config.get_string("DEFAULT", "interpreter_lang"))
            print("You said: " + data)
            self.call_function(data)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            snowboydecoder.play_audio_file("resources/error.wav")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            snowboydecoder.play_audio_file("resources/error.wav")

    def call_function(self, data):
        data = data.lower()

        if _("command.weather") in data:
            Speaker.talk(self.weather.get_one_day())
        elif data == _('command.film.pause'):
            self.kodi.pause()
        elif data == _("command.film.resume") or data == _("command.film.play"):
            self.kodi.resume()
        elif data == _("command.film.status"):
            self.kodi.film_status()
        elif _("command.date.hour") in data:
            self.calendar.get_time()
        else:
            Speaker.talk(_("speak.command.unknown"))
