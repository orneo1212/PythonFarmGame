import os
import random
import time

from xml.etree import ElementTree as ET

from farmlib.seed import Seed, seeds
from farmlib.seed import DictMapper
from farmlib.farmobject import FarmObject, objects

class FarmField:

    def __init__(self):
        """ Init FarmField"""

        self.farmtiles = {}

    def get_farmtile(self, posx, posy):
        """Get farmtile from given position"""

        arg = str(posx) + 'x' + str(posy)
        if self.farmtiles.has_key(arg):
            return self.farmtiles[arg]

        else:
            self.farmtiles[arg] = self.newfarmtile()
            return self.farmtiles[arg]

    def set_farmtile(self, posx, posy, farmtile):
        """Set farmtile at given position"""

        arg = str(posx) + 'x' + str(posy)
        self.farmtiles[arg] = farmtile

    def newfarmtile(self, farmobject = None):
        """return new farmtile with keys set"""
        ft = {"water":0, "object":farmobject}
        return ft

    def plant(self, posx, posy, seed):
        """Plant a seed on the given farmtile position"""

        farmtile = self.get_farmtile(posx, posy)
        if not farmtile['object'] and isinstance(seed, Seed):
            #plant a new seed on empty place
            farmtile['object'] = seed
            seed.start_grow()
        else:
            return 1 #  error there something on that position

    def harvest(self, posx, posy, player):
        """Harvest growed seed from farmtile"""

        farmtile = self.get_farmtile(posx, posy)
        if not farmtile["object"]:return False

        if farmtile["object"].type == "seed":
            if not farmtile['object'].growing and \
                farmtile['object'].to_harvest:
                #harvest seeds
                for i in range(farmtile['object'].growquantity):
                    #
                    player.event_harvest(farmtile['object'])

                    itemid = farmtile['object'].id
                    if itemid not in player.inventory:
                        player.inventory.append(itemid)
                        player.itemscounter[str(itemid)] = 1
                    else:
                        player.itemscounter[str(itemid)] += 1
                #TODO: add feature to many years seeds
                farmtile['object'] = None
                farmtile['water'] = 0
                return True

    def removewilted(self, posx, posy, player):
        self.remove(posx, posy, player)

    def remove(self, posx, posy, player):
        self.set_farmtile(posx, posy, self.newfarmtile())

    def water(self, posx, posy):
        """Watering a farm tile"""

        farmtile = self.get_farmtile(posx, posy)
        if farmtile["object"] is None:return False
        if farmtile["object"].type != "seed":return False

        #only one per seed
        if farmtile['water'] < 100:
            farmtile['water'] = 100 #  min(farmtile['water']+10,100)
            watereffect = int(0.2 * farmtile['object'].growtime)
            farmtile['object'].growendtime -= watereffect
            return True
        else:return False

    def create_random_anthill(self, farmtile):
        fobject = FarmObject()
        fobject.id = 1
        fobject.apply_dict(objects[fobject.id])
        farmtile["object"] = fobject

    #UPDATE
    def update(self):
        """update a farmtiles"""

        modified = False

        #update each farmtile
        for farmtile in self.farmtiles.values():
            if farmtile['object']:
                ret = farmtile['object'].update(farmtile)
                if ret:modified = True
            else:
                chance = random.randint(0, 20)
                if chance == 1 and int(time.time()) % 1800 == 0:
                    self.create_random_anthill(farmtile)
                    return True
        return modified

    def save_farmfield(self, filename, player):
        data = DictMapper()
        data["inventory"] = player.inventory
        data["itemscounter"] = player.itemscounter
        data["money"] = player.money
        data["tiles"] = []

        #fill tiles
        for ftt in self.farmtiles.keys():
            ft = self.farmtiles[ftt]
            #skip when no seed
            if not ft['object']:continue

            gameobject = ft['object']
            tile = {}
            tile["px"] = int(ftt.split('x')[0])
            tile["py"] = int(ftt.split('x')[1])
            tile["water"] = ft["water"]

            tile["object"] = {}
            #seed data
            tile["object"]["type"] = gameobject.type
            tile["object"]['id'] = gameobject.id

            if gameobject.type == "seed":
                tile["object"]['growstarttime'] = gameobject.growstarttime
                tile["object"]['growendtime'] = gameobject.growendtime
                tile["object"]['growing'] = bool(gameobject.growing)
                tile["object"]['wilted'] = bool(gameobject.wilted)
                tile["object"]['to_harvest'] = bool(gameobject.to_harvest)
            #set tile
            data["tiles"].append(tile)
        #save data
        data.save("field.json")
        return True

    def load_farmfield(self, filename, player):
        if not os.path.isfile(filename):return False
        data = DictMapper()
        data.load(filename)
        player.inventory = data["inventory"]
        player.itemscounter = data["itemscounter"]
        player.money = data["money"]
        #load tiles
        for tile in data["tiles"]:
            px = tile["px"]
            py = tile["py"]
            #Port from old saves
            if "seed" in tile:
                tile["object"] = tile["seed"]
                tile["object"]["type"] == "seed"
            #Avoid null objects
            if not tile["object"]:continue

            #Restore seed or object
            if tile["object"]["type"] == "seed":
                newseed = Seed()
                newseed.id = tile["object"]["id"]
                newseed.type = tile["object"]["type"]

                newseed.to_harvest = tile["object"]["to_harvest"]
                newseed.wilted = tile["object"]["wilted"]
                newseed.growing = tile["object"]["growing"]
                newseed.growendtime = tile["object"]["growendtime"]
                newseed.growstarttime = tile["object"]["growstarttime"]

                farmtile = self.newfarmtile(newseed)
                farmtile["water"] = tile["water"]
                newseed.apply_dict(seeds[newseed.id])
            else:
                newobject = FarmObject()
                newobject.id = tile["object"]["id"]
                newobject.type = tile["object"]["type"]
                newobject.apply_dict(objects[newobject.id])
                farmtile = self.newfarmtile(newobject)
            #set farmtile
            self.set_farmtile(px, py, farmtile)
        #return
        return True
