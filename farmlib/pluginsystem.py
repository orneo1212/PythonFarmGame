"""
Plugin system with logging support
Author: orneo1212 <orneo1212@gmail.com>
Licence: GPLv3
Version: 0.2.1
"""

#CHANGELOG
# 0.2.1 (06.06.2012)
#   = fixed call handlers
#
# 0.2 (18.01.2012)
#   + Global Hooks
#   + Unittest tests
#
# 0.1 (17.01.2012)
#   + BasePlugin
#   + BasePluginSystem
#   + Basic Event

import logging


#################
# Constans
#################
PRIORITY_LOW = -10
PRIORITY_NORMAL = 0
PRIORITY_HIGH = 10


#################
# EVENT
#################
class Event:
    """
    Base event
    Event name will be lowercase
    """
    def __init__(self, name, **args):
        self.name = name.lower()
        self.args = args
        self.priority = PRIORITY_NORMAL

    def __str__(self):
        return "Event:%s Priority:%i Args:%s" % (
            str(self.name), self.priority, str(self.args)
            )


#################
# LISTENER
#################
class Listener:
    """
    Base listener
    """
    def __init__(self, plugin):
        self.plugin = plugin
        self.eventdef = {} # dict for supported events for listener

    def isEventSupported(self, eventname):
        """
        Return True when eventname is supported by this listener
        """
        if eventname in self.eventdef:return True
        else:return False

    def getEventPriority(self, eventname):
        """
        return event priority for eventname.Return None when eventname
        not definied in supported events
        """
        if eventname in self.eventdef:return self.eventdef[eventname]
        else:return None

    def applyPriority(self, event):
        """Apply listener priority to event only when event in eventdef"""
        try:
            event.priority = self.eventdef[event.name]
            return True
        except KeyError:
            return False

    def _handleEvent(self, event):
        #call handler (handler_<eventname>)
        handler = getattr(self, "handler_%s" % event.name, None)
        if handler:
            handler(**event.args)
        else:
            print ("Handler for event %s not found" % event.name)


#################
# PLUGIN
#################
class BasePlugin:
    """
    Base Plugin
    """
    name = "nonameplugin"
    version = "0.0"

    def __init__(self):
        """Init base plugin"""
        self.system = None #Plugin system object when installed

    def registerGlobalHook(self, hookname, function):
        """Register Function globally."""
        try:
            self.system.globalhooks[hookname] = function
        except:
            msg = "Cannot Register Global Hook %s (Plugin installed?)" % hookname
            if self.system and self.system.debug:print msg


#################
# PLUGINSYSTEM
#################
class PluginSystem:
    """
    Plugin system. Only one instance for application.
    """
    def __init__(self):
        self.eventqueue = [] # Event queue
        self._plugins = [] # Plugins list
        self._listeners = [] # Listeners tuple
        self.globalhooks = {} # Dict for global hooks
        self.debug = True

    def getLogger(self, loggername):
        fileHandler = logging.FileHandler(filename = '%s.log' % str(loggername))
        formatter = logging.Formatter('%(asctime)-6s %(levelname)s - %(message)s')
        fileHandler.setFormatter(formatter)
        logger = logging.getLogger(loggername)
        logger.addHandler(fileHandler)
        return logger

    def registerEvent(self, eventname, listener, priority = PRIORITY_NORMAL):
        """Register event in listener"""
        listener.eventdef[eventname] = priority
        #Add listener to plugin system
        if listener not in self._listeners:
            self._listeners.append(listener)

    def installPlugin(self, pluginObject):
        """
        Add plugin to system.
        Call this Before emit events otherwise you cant register global
        hooks.
        """
        try:
            plugin = pluginObject()
            plugin.system = self

            #Setup plugin
            try:plugin.setup()
            except Exception, e:
                if self.debug:print e

            self._plugins.append(plugin)
            self.emit_event("pluginload", pluginname = plugin.name)
            return plugin
        except AttributeError:
            msg = "Can't install plugin from %s." % str(pluginObject)
            if self.debug:print msg

    def run(self):
        """
        Send events to plugins. This should be called with tick delay
        """
        #Set priority for events
        tempqueue = []
        for nr in xrange(len(self.eventqueue)):
            ev = self.eventqueue.pop(0)
            for listener in self._listeners:
                done = listener.applyPriority(ev)
                if done:break
            tempqueue.append(ev)
        #Set new sorted queue
        self.eventqueue = tempqueue
        #Sort events
        self.eventqueue.sort(key = lambda x:x.priority)
        #Handle events
        for nr in xrange(len(self.eventqueue)):
            ev = self.eventqueue.pop(0)
            for listener in self._listeners:
                listener.applyPriority(ev)
                listener._handleEvent(ev)

    def emit(self, event):
        """Emit event"""
        if isinstance(event, Event):
            self.eventqueue.append(event)

    def emit_event(self, eventname, **args):
        """
        Emit event by name and args (object Event will be created)
        """
        event = Event(eventname, **args)
        self.emit(event)

    def getGlobalHook(self, hookname):
        """Get Global Hook Function"""
        try:return self.globalhooks[hookname]
        except KeyError:
            msg = "Cannot get Global Hook %s" % hookname
            if self.debug:print msg


###########
###########
basePluginSystem = PluginSystem()
