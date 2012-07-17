'''
Created on 17-07-2012

@author: orneo1212
'''
import time

from farmlib.farm import FarmField
from farmlib.player import Player

class GameManager:
    def __init__(self):
        self.farms = []
        self.gametime = int(time.time())
        self.player = Player()

    def getfarm(self, farmid):
        if len(self.farms) == 0:
            self.addfarm()
        try:
            return self.farms[farmid]
        except KeyError:
            return None

    def addfarm(self):
        newfarm = FarmField()
        self.farms.append(newfarm)
        return newfarm

    def getplayer(self):
        return self.player

    def update(self):
        """should be called 20 times per second"""
        #update selected item
        if self.player.selecteditem is not None and \
            not self.player.item_in_inventory(self.player.selecteditem):
            #clear selected item if player dont have it
            self.player.selecteditem = None
        #update farms
        for farm in self.farms:
            farm.update()

    def start_new_game(self):
        #self.farms = []
        farm = self.getfarm(0)
        farm.generate_random_stones()
        farm.generate_random_planks()

    def savegame(self):
        farm = self.getfarm(0)
        farm.save_farmfield('field.json', self.player)

    def loadgame(self):
        farm = self.getfarm(0)
        result = farm.load_farmfield('field.json', self.player)
        return result

    def timeforward(self):
        farm = self.getfarm(0)
        if farm.seconds_to_update>1000:
            farm.seconds_to_update=1000
        if farm.seconds_to_update:
            #1 second is equal 20 updates
            for _ in xrange(farm.seconds_to_update):
                self.update()
