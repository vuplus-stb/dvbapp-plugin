#
# Warning: This Plugin is WIP
#

# GUI (Screens)
from Screens.MessageBox import MessageBox
from AutoTimerOverview import AutoTimerOverview

# Plugin
from AutoTimer import AutoTimer
from AutoPoller import autopoller

# Plugin definition
from Plugins.Plugin import PluginDescriptor

# ExpatError
from xml.parsers.expat import ExpatError

# Config
from Components.config import config, ConfigSubsection, ConfigEnableDisable, ConfigInteger, ConfigSelection

# Initialize Configuration
config.plugins.autotimer = ConfigSubsection()
config.plugins.autotimer.autopoll = ConfigEnableDisable(default = False)
config.plugins.autotimer.interval = ConfigInteger(default = 3, limits=(1, 24))
config.plugins.autotimer.refresh = ConfigSelection(choices = [("none", _("None")), ("auto", _("Only AutoTimers created during this Session")), ("all", _("All non-repeating Timers"))], default = "none")
config.plugins.autotimer.try_guessing = ConfigEnableDisable(default = False)

autotimer = None

# Autostart
def autostart(reason, **kwargs):
	global autotimer

	# Startup
	if config.plugins.autotimer.autopoll.value and reason == 0:
		# Initialize AutoTimer
		autotimer = AutoTimer()

		# Start Poller
		autopoller.start(autotimer)
	# Shutdown
	elif reason == 1:
		# Stop Poller
		autopoller.stop()

		if autotimer is not None:
			# Save xml
			autotimer.writeXml()

			# Remove AutoTimer
			autotimer = None

# Mainfunction
def main(session, **kwargs):
	global autotimer
	if autotimer is None:
		autotimer = AutoTimer()

	try:
		autotimer.readXml()
	except ExpatError, ee:
		session.open(
			MessageBox,
			"Your config file is not well-formed.\nError parsing in line: %s" % (ee.lineno),
			type = MessageBox.TYPE_ERROR,
			timeout = 10
		)
		return
	except Exception, e:
		# Don't crash during development
		import traceback, sys
		traceback.print_exc(file=sys.stdout)
		session.open(
			MessageBox,
			"An unexpected error occured: %s" % (e),
			type = MessageBox.TYPE_ERROR,
			timeout = 15
		)
		return

	# Do not run in background while editing, this might screw things up
	autopoller.stop()

	session.openWithCallback(
		editCallback,
		AutoTimerOverview,
		autotimer
	)

def editCallback(session):
	global autotimer

	if config.plugins.autotimer.autopoll.value:
		autopoller.start(autotimer, initial = False)

	# Don't do anything when editing was canceled
	if session is None:
		return

	# We might re-parse Xml so catch parsing error
	try:
		ret = autotimer.parseEPG()
		session.open(
			MessageBox,
			"Found a total of %d matching Events.\n%d Timer were added and %d modified.." % (ret[0], ret[1], ret[2]),
			type = MessageBox.TYPE_INFO,
			timeout = 10
		)
	except Exception, e:
		# Don't crash during development
		import traceback, sys
		traceback.print_exc(file=sys.stdout)
		session.open(
			MessageBox,
			"An unexpected error occured: %s" % (e),
			type = MessageBox.TYPE_ERROR,
			timeout = 15
		)

def Plugins(**kwargs):
	return [
		PluginDescriptor(where = PluginDescriptor.WHERE_AUTOSTART, fnc = autostart),
		PluginDescriptor(name="AutoTimer", description = "Edit Timers and scan for new Events", where = PluginDescriptor.WHERE_PLUGINMENU, icon = "plugin.png", fnc = main),
		PluginDescriptor(name="AutoTimer", description = "Edit Timers and scan for new Events", where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc = main)
	]