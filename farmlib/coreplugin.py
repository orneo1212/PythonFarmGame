from __init__ import rules
from pluginsystem import BasePlugin, Listener

REMOVEWILTEDCOST = rules["REMOVEWILTEDCOST"]
REMOVEANTHILLCOST = rules["REMOVEANTHILLCOST"]
REMOVESTONECOST = rules["REMOVESTONECOST"]

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
        print ("Tool %s used on %s" % (toolname, str(position)))
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
        """Harvest events"""
        done = farm.harvest(position[0], position[1], player)
        if done:self.plugin.gamewindow.regenerate_groups()

    def pickaxe_events(self, farm, player, position):
        """Pickaxe events"""
        farmobject = farm.get_farmobject(position[0], position[1])
        if not farmobject:return

        #Remove stones
        if farmobject.type != "seed" and \
            farmobject.id == 6 and self.player.money >= REMOVESTONECOST:
            player.money -= REMOVESTONECOST
            farm.remove(position[0], position[1], player)
            #regenerate sprites
            self.plugin.gamewindow.regenerate_groups()


    def shovel_events(self, farm, player, position):
        """Shovel events"""
        farmobject = farm.get_farmobject(position[0], position[1])
        if not farmobject:return

        #Remove anthill
        if farmobject.id == 7 and player.money >= REMOVEANTHILLCOST:
            player.money -= REMOVEANTHILLCOST
            farm.remove(position[0], position[1], player)
            self.plugin.gamewindow.regenerate_groups()

        #Remove wilted
        if farmobject.id == 8 and player.money >= REMOVEWILTEDCOST:
            player.money -= REMOVEWILTEDCOST
            farm.removewilted(position[0], position[1], player)
            self.plugin.gamewindow.regenerate_groups()
        #remove seed
        if farmobject and farmobject.type == "seed":
            #remove seed when is NOT ready
            if not farmobject.to_harvest:
                farm.remove(position[0], position[1], player)
            #regenerate sprites
            self.plugin.gamewindow.regenerate_groups()

    def axe_events(self, farm, player, position):
        """Axe events"""
        farmobject = farm.get_farmobject(position[0], position[1])
        if not farmobject:return

        #Remove planks
        removeplankcost = rules["REMOVEPLANKCOST"]
        if farmobject.id == 9 and player.money >= removeplankcost:
            player.money -= removeplankcost
            farm.remove(position[0], position[1], player)
            self.plugin.gamewindow.regenerate_groups()
