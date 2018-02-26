#-*- coding: utf-8 -*-
import snowboydecoder
from interpreter import Interpreter
from config import Config

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