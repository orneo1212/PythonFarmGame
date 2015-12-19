from __future__ import absolute_import

from farmlib import rules
from farmlib.pluginsystem import BasePlugin, Listener

REMOVEWILTEDCOST = rules["REMOVEWILTEDCOST"]
REMOVEANTHILLCOST = rules["REMOVEANTHILLCOST"]
REMOVESTONECOST = rules["REMOVESTONECOST"]


class CorePlugin(BasePlugin):
    """
    CorePlugin
    """
    name = "coreplugin"
    version = "0.3"

    def __init__(self):
        BasePlugin.__init__(self)

    def setup(self):
        """setup

        :return:
        """
        self.listener = CoreListener(self)
        self.system.register_event("toolused", self.listener)


class CoreListener(Listener):
    """
    CoreListener
    """
    def __init__(self, plugin):
        Listener.__init__(self, plugin)

    @staticmethod
    def handler_pluginload(pluginname):
        """handler pluginload

        :param pluginname:
        :return:
        """
        print(pluginname)

    def handler_toolused(self, position, gamemanager):
        """Tool used on

        :param position:
        :param gamemanager:
        :return:
        """
        player = gamemanager.getplayer()
        farm = gamemanager.getfarm()
        toolname = player.selectedtool
        # print("Tool {0} used on {1}".format(toolname, str(position)))
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

    @staticmethod
    def watercan_events(farm, player, position):
        """watercan events

        :param farm:
        :param player:
        :param position:
        :return:
        """
        if not player.watercanuses:
            False
        done = farm.water(position[0], position[1])
        if not done:
            return False

        player.event_water()
        player.watercanuses -= 1

    @staticmethod
    def plant_events(farm, player, position):
        """plant events

        :param farm:
        :param player:
        :param position:
        :return:
        """
        done = False

        selecteditem = player.selecteditem
        newobject = player.create_new_object_by_id(selecteditem)

        if not newobject:
            player.selecteditem = None

        # check player level
        elif player.level >= newobject.requiredlevel:
            done = farm.plant(position[0], position[1], newobject)
            if done:
                player.remove_item(newobject.id)

    @staticmethod
    def harvest_events(farm, player, position):
        """Harvest events"""
        farm.harvest(position[0], position[1], player)

    @staticmethod
    def pickaxe_events(farm, player, position):
        """Pickaxe events"""
        farmobject = farm.get_farmobject(position[0], position[1])
        if not farmobject:
            return

        # Remove stones
        if farmobject.type != "seed" and \
                farmobject.id == 6 and player.money >= REMOVESTONECOST:
            player.money -= REMOVESTONECOST
            farm.remove(position[0], position[1], player)

    @staticmethod
    def shovel_events(farm, player, position):
        """Shovel events"""
        farmobject = farm.get_farmobject(position[0], position[1])
        if not farmobject:
            return

        # Remove anthill
        if farmobject.id == 7 and player.money >= REMOVEANTHILLCOST:
            player.money -= REMOVEANTHILLCOST
            farm.remove(position[0], position[1], player)

        # Remove wilted
        if farmobject.id == 8 and player.money >= REMOVEWILTEDCOST:
            player.money -= REMOVEWILTEDCOST
            farm.removewilted(position[0], position[1])

        # Pickup pond
        if farmobject.id == 11:
            farm.set_farmobject(position[0], position[1], None)
            player.add_item(11)

        # remove seed
        if farmobject and farmobject.type == "seed"\
                and not farmobject.to_harvest:
            # remove seed when is NOT ready
            farm.remove(position[0], position[1], player)

    @staticmethod
    def axe_events(farm, player, position):
        """Axe events"""
        farmobject = farm.get_farmobject(position[0], position[1])
        if not farmobject:
            return

        # Remove planks
        removeplankcost = rules["REMOVEPLANKCOST"]
        if farmobject.id == 9 and player.money >= removeplankcost:
            player.money -= removeplankcost
            farm.remove(position[0], position[1], player)
