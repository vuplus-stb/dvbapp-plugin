# -*- coding: utf-8 -*-
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from os import environ as os_environ
import gettext

def localeInit():
	lang = language.getLanguage()[:2] # getLanguage returns e.g. "fi_FI" for "language_country"
	os_environ["LANGUAGE"] = lang # Enigma doesn't set this (or LC_ALL, LC_MESSAGES, LANG). gettext needs it!
	gettext.bindtextdomain("MovieRetitle", resolveFilename(SCOPE_PLUGINS, "Extensions/MovieRetitle/locale"))

def _(txt):
	t = gettext.dgettext("MovieRetitle", txt)
	if t == txt:
		print(("[MovieRetitle] fallback to default translation for", txt))
		t = gettext.gettext(txt)
	return t

localeInit()
language.addCallback(localeInit)

