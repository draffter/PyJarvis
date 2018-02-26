# -*- coding: utf-8 -*-
from ConfigParser import SafeConfigParser
import codecs

class Config(object):
    def __init__(self):
        self.config = SafeConfigParser()
        self.parse_config()

    def parse_config(self):
        with codecs.open('config.ini', 'r', encoding='utf-8') as f:
            self.config.readfp(f)

    def get_string(self, section, option):
        return self.config.get(section, option).encode('utf-8')

    def get_int(self, section, option):
        return self.config.getint(section, option)