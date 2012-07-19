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

    def handler_toolused(self, position, gamemanager):
        #print ("Tool %s used on %s" % (toolname, str(position)))
        player = gamemanager.getplayer()
        farm = gamemanager.getfarm()
        toolname = player.selectedtool
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
        if not player.watercanuses:return False
        done = farm.water(position[0], position[1])
        if not done:return False

        player.watercanuses -= 1

    def plant_events(self, farm, player, position):
        done = False

        selecteditem = player.selecteditem
        newobject = player.create_new_object_by_id(selecteditem)

        if not newobject:
            player.selecteditem = None

        #check player level
        elif player.level >= newobject.requiredlevel:
            done = farm.plant(position[0], position[1], newobject)
            if done:player.remove_item(newobject.id)

    def harvest_events(self, farm, player, position):
        """Harvest events"""
        farm.harvest(position[0], position[1], player)

    def pickaxe_events(self, farm, player, position):
        """Pickaxe events"""
        farmobject = farm.get_farmobject(position[0], position[1])
        if not farmobject:return

        #Remove stones
        if farmobject.type != "seed" and \
            farmobject.id == 6 and player.money >= REMOVESTONECOST:
            player.money -= REMOVESTONECOST
            farm.remove(position[0], position[1], player)

    def shovel_events(self, farm, player, position):
        """Shovel events"""
        farmobject = farm.get_farmobject(position[0], position[1])
        if not farmobject:return

        #Remove anthill
        if farmobject.id == 7 and player.money >= REMOVEANTHILLCOST:
            player.money -= REMOVEANTHILLCOST
            farm.remove(position[0], position[1], player)

        #Remove wilted
        if farmobject.id == 8 and player.money >= REMOVEWILTEDCOST:
            player.money -= REMOVEWILTEDCOST
            farm.removewilted(position[0], position[1], player)
        #remove seed
        if farmobject and farmobject.type == "seed":
            #remove seed when is NOT ready
            if not farmobject.to_harvest:
                farm.remove(position[0], position[1], player)

    def axe_events(self, farm, player, position):
        """Axe events"""
        farmobject = farm.get_farmobject(position[0], position[1])
        if not farmobject:return

        #Remove planks
        removeplankcost = rules["REMOVEPLANKCOST"]
        if farmobject.id == 9 and player.money >= removeplankcost:
            player.money -= removeplankcost
            farm.remove(position[0], position[1], player)
