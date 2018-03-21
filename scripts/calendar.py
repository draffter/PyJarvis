# -*- coding: utf-8 -*-
from datetime import datetime
from speaker import Speaker
from translator import ngettext

class Calendar(object):

    def get_time(self):
        now = datetime.now()
        Speaker.talk(_("speak.calendar.hour %s ") % format("%d:%d" % (now.hour, now.minute)))
