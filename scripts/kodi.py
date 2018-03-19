# -*- coding: utf-8 -*-
import requests
import json
import urllib
from speaker import Speaker


class Kodi(object):
    def __init__(self, host="localhost", port="8888"):
        self.headers = {'content-type': 'application/json'}
        self.json_rpc_url = "http://" + host + ":" + str(port) + "/jsonrpc"
        self._reset_player_status()

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
                speed_data = self._send("Player.GetProperties",
                                        params={"playerid": self.player_id, "properties": ["speed"]})
                if "speed" in speed_data["result"]:
                    self.paused = speed_data["result"]["speed"] == 0

    def pause(self):
        self._get_player_status()
        if self.paused:
            Speaker.talk(u"film jest zatrzymany")
        if not self.playing:
            Speaker.talk(u"nic nie jest odtwarzane")
        else:
            self._send("Player.PlayPause", {"playerid": self.player_id})

    def resume(self):
        self._get_player_status()
        if not self.playing:
            Speaker.talk(u"nic nie jest odtwarzane")
        elif not self.paused:
            Speaker.talk(u"film nie jest zatrzymany")
        else:
            self._send("Player.PlayPause", {"playerid": self.player_id})

    def get_item(self):
        self._get_player_status()
        self._send("Player.GetProperties", {"properties": ["speed", "position", "time", "playlistid"], "playerid": self.player_id})
        self._send("Player.GetItem", {"properties": ["duration","title","album","artist","season","episode","showtitle","tvshowid","thumbnail","file","fanart","streamdetails"], "playerid": self.player_id})
