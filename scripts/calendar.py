# -*- coding: utf-8 -*-


from datetime import datetime
from speaker import Speaker

hours = ['dwunasta', 'pierwsza', 'druga', 'trzecia', 'czwarta', 'piąta', 'szósta', 'siódma', 'ósma', 'dziwiąta',
         'dziesiąta', 'jedenasta',
         'dwunasta', 'trzynasta', 'czternasta', 'piętnasta', 'szesnasta', 'siedemnasta', 'osiemnasta', 'dziewiętnasta',
         'dwudziesta',
         'dwudziesta pierwsza', 'dwudzesta druga', 'dwudziesta trzecia']


class Calendar(object):

    def get_time(self):
        now = datetime.now()
        Speaker.talk(u"Jest {} {}".format(hours[now.hour], now.minute))
