# -*- coding: utf-8 -*-
import gettext
import os
import locale
from config import Config

config = Config()
localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
app_name = 'jarvis'
gettext.textdomain(app_name)
gettext.bindtextdomain(app_name, localedir)
locale.setlocale(locale.LC_ALL, "")
lang = config.get_string("DEFAULT", "interpreter_lang")
translate = gettext.translation(app_name, localedir, languages=[lang], fallback=True)
translate.install(unicode=True)
_ = translate.gettext


def ngettext(msgid1, msgid2, n):
    return translate.ngettext(msgid1, msgid2, n)
