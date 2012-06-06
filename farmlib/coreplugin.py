from pluginsystem import BasePlugin, Listener

class CorePlugin(BasePlugin):
    name = "coreplugin"
    version = "0.3"

    def __init__(self):
        BasePlugin.__init__(self)

    def setup(self):
        self.listener = CoreListener(self)
        self.system.registerEvent("toolused", self.listener)

class CoreListener(Listener):
    def __init__(self, plugin):
        Listener.__init__(self, plugin)

    def handler_pluginload(self, pluginname):
        pass

    def handler_toolused(self, toolname, farm, position):
        #print ("Tool %s used on %s" % (toolname, str(position)))
        if toolname == "watering":
            self.watercan_events(farm, position)
        if toolname == "plant":
            self.plant_events(farm, position)
        if toolname == "harvest":
            self.harvest_events(farm, position)
        if toolname == "pickaxe":
            self.pickaxe_events(farm, position)
        if toolname == "shovel":
            self.shovel_events(farm, position)
        if toolname == "axe":
            self.axe_events(farm, position)

    def watercan_events(self, farm, position):
        pass

    def plant_events(self, farm, position):
        pass

    def harvest_events(self, farm, position):
        pass

    def pickaxe_events(self, farm, position):
        pass

    def shovel_events(self, farm, position):
        pass

    def axe_events(self, farm, position):
        pass
