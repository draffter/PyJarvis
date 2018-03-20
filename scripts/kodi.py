# -*- coding: utf-8 -*-
import requests
import json
import urllib
from speaker import Speaker
from translator import ngettext
from datetime import datetime, timedelta
from config import Config

class KodiException(Exception):
    pass

class Kodi(object):
    def __init__(self, host="localhost", port="8888"):
        self.headers = {'content-type': 'application/json'}
        self.json_rpc_url = "http://" + host + ":" + str(port) + "/jsonrpc"
        self._reset_player_status()
        self.get_languages()

    # noinspection PyAttributeOutsideInit
    def get_languages(self):
        config = Config()
        self.same_language = True
        self.library_language = config.get_string('KODI', 'library_tts_language')
        self.tts_language = config.get_string('DEFAULT', 'tts_lang')
        if self.tts_language != self.library_language:
            self.same_language = False

    # noinspection PyAttributeOutsideInit
    def _reset_player_status(self):
        self.playing = False
        self.paused = False
        self.player_id = None

    def _send(self, method, params={}, id=1):
        payload = {"jsonrpc": "2.0", "method": method, "id": id, "params": params}
        url_param = urllib.urlencode({'request': json.dumps(payload)})
        print self.json_rpc_url + '?' + url_param
        response = requests.get(self.json_rpc_url + '?' + url_param, headers=self.headers)
        print response.text
        return json.loads(response.text)

    def _get_player_status(self):
        self._reset_player_status()
        data = self._send("Player.GetActivePlayers")
        if data['result']:
            self.playing = len(data['result']) > 0
            if self.playing:
                self.player_id = data['result'][0]["playerid"]
                speed_data = self._send("Player.GetProperties", params={"playerid": self.player_id, "properties": ["speed"]})
                if "speed" in speed_data["result"]:
                    self.paused = speed_data["result"]["speed"] == 0

    def pause(self):
        self._get_player_status()
        if self.paused:
            Speaker.talk(_("movie.is_stopped"))
        if not self.playing:
            Speaker.talk(_("movie.nothing_played"))
        else:
            self._send("Player.PlayPause", {"playerid": self.player_id})

    def resume(self):
        self._get_player_status()
        if not self.playing:
            Speaker.talk(_("movie.nothing_played"))
        elif not self.paused:
            Speaker.talk(_("movie.is_not_paused"))
        else:
            self._send("Player.PlayPause", {"playerid": self.player_id})

    def film_status(self):
        self._get_player_status()
        if not self.playing:
            Speaker.talk(_("movie.nothing_played"))
        else:
            try:
                movie_name = self.get_movie_name()
                movie_time = self.get_movie_time()
                if self.same_language:
                    s =_("movie.watching %s ") % movie_name + _("movie.end_time %s") % movie_time
                    Speaker.talk(s)
                else:
                    Speaker.add_text(_("movie.watching %s ") % "", self.tts_language)
                    Speaker.add_text(movie_name, self.library_language)
                    Speaker.add_text( _("movie.end_time %s") % movie_time, self.tts_language)
                    Speaker.make_out_file()
                    Speaker.play()

            except KodiException:
                Speaker.talk(_("kodi.error"))

    def get_movie_name(self):
        movie_item = self._send("Player.GetItem", {"properties": ["title"], "playerid": self.player_id})
        if movie_item['result']:
            if movie_item['result']['item']:
                if movie_item['result']['item']['title']:
                    return movie_item['result']['item']['title']
        raise KodiException

    def get_movie_time(self):
        movie_time = self._send("Player.GetProperties", {"properties": ["time", "totaltime"], "playerid": self.player_id})
        if movie_time['result']:
            if movie_time['result']['time']:
                if movie_time['result']['totaltime']:
                    end_hour = datetime.now() - timedelta(hours=movie_time['result']['time']['hours'], minutes=movie_time['result']['time']['minutes'], seconds=movie_time['result']['time']['seconds']) + timedelta(hours=movie_time['result']['totaltime']['hours'], minutes=movie_time['result']['totaltime']['minutes'], seconds=movie_time['result']['totaltime']['seconds'])
                    return format(end_hour, '%H:%M')
        raise KodiException
