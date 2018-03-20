# -*- coding: utf-8 -*-
from gtts import gTTS
import os, glob
from config import Config
import shutil


class Speaker(object):
    lang = None
    index = 1

    @staticmethod
    def talk(speech_string):
        print(speech_string)
        if Speaker.lang is None:
            Speaker.get_language()
        tts = gTTS(text=speech_string, lang=Speaker.lang)
        tts.save("audio/audio.mp3")
        Speaker.play()

    @staticmethod
    def play():
        os.system("mpg321 audio/audio.mp3")
        Speaker.clear_directory()

    @staticmethod
    def clear_directory():
        file_list = glob.glob(os.path.join('audio', "*.mp3"))
        for f in file_list:
            os.remove(f)

    @staticmethod
    def make_out_file():
        destination = open('audio/audio.mp3', 'wb')
        file_list = sorted(glob.glob(os.path.join('audio', "*.mp3")))
        for f in file_list:
            shutil.copyfileobj(open(f, 'rb'), destination)
        destination.close()

    @staticmethod
    def add_text(text, lang):
        tts = gTTS(text=text, lang=lang)
        print "audio/audio_%d.mp3 %s" % (Speaker.index, text)
        tts.save("audio/audio_%d.mp3" % Speaker.index)
        Speaker.index += 1

    @classmethod
    def get_language(cls):
        config = Config()
        Speaker.lang = config.get_string("DEFAULT", "tts_lang")
