import os

from xml.etree import ElementTree as ET

from farmlib.seed import Seed, seeds
from farmlib.seed import DictMapper

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
            self.farmtiles[arg] = {'water':0, 'seed':None}
            return self.farmtiles[arg]

    def set_farmtile(self, posx, posy, farmtile):
        """Set farmtile at given position"""

        arg = str(posx) + 'x' + str(posy)
        self.farmtiles[arg] = farmtile

    def plant(self, posx, posy, seed):
        """Plant a seed on the given farmtile position"""

        farmtile = self.get_farmtile(posx, posy)
        if not farmtile['seed'] and seed:
            #plant a new seed on empty place
            farmtile['seed'] = seed
            seed.start_grow()
        else:
            return 1 #  error there something on that position

    def harvest(self, posx, posy, player):
        """Harvest growed seed from farmtile"""

        farmtile = self.get_farmtile(posx, posy)
        if farmtile['seed']:
            if not farmtile['seed'].growing and farmtile['seed'].to_harvest:
                #harvest seeds
                for i in range(farmtile['seed'].growquantity):
                    #
                    player.event_harvest(farmtile['seed'])

                    itemid = farmtile['seed'].id
                    if itemid not in player.inventory:
                        player.inventory.append(itemid)
                        player.itemscounter[str(itemid)] = 1
                    else:
                        player.itemscounter[str(itemid)] += 1
                #TODO: add feature to many years seeds
                farmtile['seed'] = None
                farmtile['water'] = 0

    def removewilted(self, posx, posy, player):
        self.remove(posx, posy, player)

    def remove(self, posx, posy, player):
        farmtile = self.get_farmtile(posx, posy)
        farmtile['seed'] = None
        farmtile['water'] = None

    def water(self, posx, posy):
        """Watering a farm tile"""

        farmtile = self.get_farmtile(posx, posy)
        #only one per seed
        if farmtile['water'] < 100:
            farmtile['water'] = 100 #  min(farmtile['water']+10,100)
            watereffect = int(0.2 * farmtile['seed'].growtime)
            farmtile['seed'].growendtime -= watereffect
            return True
        else:return False

    def status(self, posx, posy):
        """Status"""

        farmtile = self.get_farmtile(posx, posy)
        if farmtile['seed']:
            print farmtile['seed'].name, "-", farmtile['seed'].description, "[ End in.", farmtile['seed'].remainstring, "]"

    #UPDATE
    def update(self):
        """update a farmtiles"""

        modified = False

        #update each farmtile
        for farmtile in self.farmtiles.values():
            if farmtile['seed']:
                ret = farmtile['seed'].update(farmtile)
                if ret:modified = True
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
            if not ft['seed']:continue

            gameobject = ft['seed']
            tile = {}
            tile["px"] = int(ftt.split('x')[0])
            tile["py"] = int(ftt.split('x')[1])
            tile["water"] = ft["water"]

            #Store seed if present
            if isinstance(gameobject, Seed):
                tile["seed"] = {}
                #seed data
                tile["seed"]['growstarttime'] = gameobject.growstarttime
                tile["seed"]['growendtime'] = gameobject.growendtime
                tile["seed"]['growing'] = bool(gameobject.growing)
                tile["seed"]['wilted'] = bool(gameobject.wilted)
                tile["seed"]['to_harvest'] = bool(gameobject.to_harvest)
                tile["seed"]['id'] = gameobject.id
            #Farm object
            else:
                tile["object"] = {}
                #seed data
                tile["object"]['id'] = gameobject.id
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
            if "seed" in tile:
                newseed = Seed()
                newseed.id = tile["seed"]["id"]
                newseed.to_harvest = tile["seed"]["to_harvest"]
                newseed.wilted = tile["seed"]["wilted"]
                newseed.growing = tile["seed"]["growing"]
                newseed.growendtime = tile["seed"]["growendtime"]
                newseed.growstarttime = tile["seed"]["growstarttime"]

                farmtile = {"water":tile["water"], "seed":newseed}
                newseed.apply_dict(seeds[newseed.id])
            else:
                #TODO: load farm object
                pass
            self.set_farmtile(px, py, farmtile)
        #return
        return True
