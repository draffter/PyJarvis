#-*- coding: utf-8 -*-
# !/usr/bin/python

import snowboydecoder
from interpreter import Interpreter
from config import Config
import gettext
import locale
import os

config = Config()
localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
app_name = 'jarvis'
gettext.textdomain(app_name)
gettext.bindtextdomain(app_name, localedir)
locale.setlocale(locale.LC_ALL, "")
lang = config.get_string("DEFAULT", "interpreter_lang")
translate = gettext.translation(app_name, localedir, languages=[lang], fallback = True)
translate.install(unicode=True)
_ = translate.gettext

class VoiceDetect(object):

    def __init__(self):
        self.config = Config()
        self.interpreter = Interpreter(self.config)
        self.model = "resources/JARVIS.pmdl"
        self.sensitivity = 0.5
        self.audio_gain = 1.5
        self.detector = snowboydecoder.HotwordDetector(self.model, sensitivity=self.sensitivity, audio_gain=self.audio_gain)
        self.interpreter.calibrate(self.run)

    def detect_callback(self):
        self.detector.terminate()
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
        self.interpreter.listen()
        self.run()

    def run(self):
        print "start recognizing word"
        self.detector.start(detected_callback=self.detect_callback, sleep_time=0.03)


if __name__ == '__main__':
    c = VoiceDetect()
    # my_kodi = Kodi('localhost', port=80)
    # my_kodi.Player.Stop(1)
    # print(my_kodi.Player.GetProperties(1))
    # print(my_kodi)