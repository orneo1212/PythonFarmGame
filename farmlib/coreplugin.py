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

    def handler_toolused(self, toolname, farm, player, position):
        #print ("Tool %s used on %s" % (toolname, str(position)))
        if toolname == "watering":
            self.watercan_events(farm, player, position)
        elif toolname == "plant":
            self.plant_events(farm, player, position)
        elif toolname == "harvest":
            self.harvest_events(farm, player, position)
        elif toolname == "pickaxe":
            self.pickaxe_events(farm, player, position)
        elif toolname == "shovel":
            self.shovel_events(farm, player, position)
        elif toolname == "axe":
            self.axe_events(farm, player, position)

    def watercan_events(self, farm, player, position):
        if player.watercanuses < 1:return
        done = farm.water(position[0], position[1])
        #regenerate sprites
        if done:
            player.watercanuses -= 1
            self.plugin.gamewindow.regenerate_groups()

    def plant_events(self, farm, player, position):
        pass

    def harvest_events(self, farm, player, position):
        done = self.farm.harvest(position[0], position[1], player)
        if done:self.plugin.gamewindow.regenerate_groups()

    def pickaxe_events(self, farm, player, position):
        pass

    def shovel_events(self, farm, player, position):
        pass

    def axe_events(self, farm, player, position):
        pass
