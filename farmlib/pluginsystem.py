"""
Plugin system with logging support
Author: orneo1212 <orneo1212@gmail.com>
Licence: GPLv3
Version: 0.2.1
"""

# CHANGELOG
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


# Constans
PRIORITY_LOW = -10
PRIORITY_NORMAL = 0
PRIORITY_HIGH = 10

try:
    xrange
except NameError:
    xrange = range


# EVENT
class Event(object):
    """
    Base event
    Event name will be lowercase
    """
    def __init__(self, name, **args):
        self.name = name.lower()
        self.args = args
        self.priority = PRIORITY_NORMAL

    def __str__(self):
        return "Event:{0!s} Priority:{1:d} Args:{2!s}".format(
            str(self.name), self.priority, str(self.args)
            )


# LISTENER
class Listener(object):
    """
    Base listener
    """
    def __init__(self, plugin):
        self.plugin = plugin
        self.eventdef = {}
        # dict for supported events for listener

    def is_event_supported(self, eventname):
        """
        Return True when eventname is supported by this listener
        """
        if eventname in self.eventdef:
            return True
        else:
            return False

    def get_event_priority(self, eventname):
        """
        return event priority for eventname.Return None when eventname
        not definied in supported events
        """
        if eventname in self.eventdef:
            return self.eventdef[eventname]
        else:
            return None

    def apply_priority(self, event):
        """Apply listener priority to event only when event in eventdef"""
        if event.name in self.eventdef:
            return True
        else:
            return False

    def handle_event(self, event):
        """call handler (handler_<eventname>)

        :param event:
        :return:
        """
        handler = getattr(self, "handler_{0!s}".format(event.name), None)
        if handler:
            handler(**event.args)
        else:
            print("Handler for event {0!s} not found".format(event.name))


# PLUGIN
class BasePlugin(object):
    """
    Base Plugin
    """
    name = "nonameplugin"
    version = "0.0"

    def __init__(self):
        """Init base plugin"""
        self.system = None
        # Plugin system object when installed

    def register_global_hook(self, hookname, function):
        """Register Function globally."""
        try:
            self.system.globalhooks[hookname] = function
        except KeyError:
            msg = ("Cannot Register Global"
                   " Hook {} (Plugin installed?)".format(hookname))
            if self.system and self.system.debug:
                print(msg)


#################
# PLUGINSYSTEM
#################
class PluginSystem(object):
    """
    Plugin system. Only one instance for application.
    """
    def __init__(self):
        self.eventqueue = []  # Event queue
        self._plugins = []  # Plugins list
        self._listeners = []  # Listeners tuple
        self.globalhooks = {}  # Dict for global hooks
        self.debug = True

    @staticmethod
    def get_logger(loggername):
        """logger

        :param loggername:
        :return:
        """
        filehandler = logging.FileHandler(
            filename='{0!s}.log'.format(str(loggername)))
        formatter = logging.Formatter(
            '%(asctime)-6s %(levelname)s - %(message)s')
        filehandler.setFormatter(formatter)
        logger = logging.getLogger(loggername)
        logger.addHandler(filehandler)

        return logger

    def register_event(self, eventname, listener, priority=PRIORITY_NORMAL):
        """Register event in listener"""
        listener.eventdef[eventname] = priority
        # Add listener to plugin system
        if listener not in self._listeners:
            self._listeners.append(listener)

    def install_plugin(self, pluginObject):
        """
        Add plugin to system.
        Call this Before emit events otherwise you cant register global
        hooks.
        """
        try:
            plugin = pluginObject()
            plugin.system = self

            # Setup plugin
            try:
                plugin.setup()
            except Exception as e:
                if self.debug:
                    print(e)

            self._plugins.append(plugin)
            self.emit_event("pluginload", pluginname=plugin.name)
            return plugin
        except AttributeError:
            msg = "Can't install plugin from {0!s}.".format(str(pluginObject))
            if self.debug:
                print(msg)

    def run(self):
        """
        Send events to plugins. This should be called with tick delay
        """
        # Set priority for events
        tempqueue = []
        for nr in xrange(len(self.eventqueue)):
            ev = self.eventqueue.pop(0)
            for listener in self._listeners:
                done = listener.apply_priority(ev)
                if done:
                    break
            tempqueue.append(ev)
        # Set new sorted queue
        self.eventqueue = tempqueue
        # Sort events
        self.eventqueue.sort(key=lambda x: x.priority)
        # Handle events
        for nr in xrange(len(self.eventqueue)):
            ev = self.eventqueue.pop(0)
            for listener in self._listeners:
                listener.apply_priority(ev)
                listener.handle_event(ev)

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

    def get_global_hook(self, hookname):
        """Get Global Hook Function"""
        try:
            return self.globalhooks[hookname]
        except KeyError:
            msg = "Cannot get Global Hook {0!s}".format(hookname)
            if self.debug:
                print(msg)


###########
###########
base_plugin_system = PluginSystem()
