#-*- coding: utf-8 -*-
from gtts import gTTS
import os
from config import Config


class Speaker(object):
    lang = None

    @staticmethod
    def talk(speech_string):
        print(speech_string)
        if Speaker.lang is None:
            Speaker.getLanguage()
        tts = gTTS(text=speech_string, lang=Speaker.lang)
        tts.save("audio.mp3")
        os.system("mpg321 audio.mp3")

    @classmethod
    def getLanguage(cls):
        config = Config()
        Speaker.lang = config.get_string("DEFAULT", "tts_lang")