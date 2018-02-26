#-*- coding: utf-8 -*-
import urllib2

class WebCrawler(object):

    @staticmethod
    def get_data(uri):
        response = urllib2.urlopen(uri)
        return response.read()