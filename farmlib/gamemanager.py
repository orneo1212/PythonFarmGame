'''
Created on 17-07-2012

@author: orneo1212
'''
import os
import time

from farmlib.farm import FarmField, FarmTile, FarmObject, Seed, objects
from farmlib import DictMapper
from farmlib.player import Player

class GameManager:
    def __init__(self):
        self.farms = []
        self.gameseed = int(time.time())
        self.gametime = int(time.time())
        self.current_farm = 0
        self.player = Player()

    def getfarm(self, farmid = None):
        if farmid is None:
            farmid = self.current_farm
        if len(self.farms) == 0:
            self.addfarm()
        try:
            return self.farms[farmid]
        except IndexError:
            return None

    def getfarmcount(self):
        return len(self.farms)

    def getcurrentfarmid(self):
        return self.current_farm

    def getnextfarmcost(self):
        farmcount = self.getfarmcount() - 1
        cost = 10000 + 12000 * farmcount
        return cost

    def addfarm(self):
        newfarm = FarmField(self)
        self.farms.append(newfarm)
        return newfarm

    def setcurrentfarm(self, farmid):
        if farmid > self.getfarmcount():
            farmid = self.getfarmcount() - 1
        self.current_farm = farmid
        return farmid

    def getgameseed(self):
        return self.gameseed

    def setgameseed(self, newseed):
        self.gameseed = newseed

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
        self.save_gamestate('field.json', self.player)

    def loadgame(self):
        result = self.load_gamestate('field.json', self.player)
        return result

    def timeforward(self):
        farm = self.getfarm(0)
        if farm.seconds_to_update > 1000:
            farm.seconds_to_update = 1000
        if farm.seconds_to_update:
            #1 second is equal 20 updates
            for _ in xrange(farm.seconds_to_update):
                self.update()

    def save_gamestate(self, filename, player):
        print ("Saveing game state...")
        data = DictMapper()
        #Save player data
        data["inventory"] = player.inventory
        data["itemscounter"] = player.itemscounter
        data["money"] = player.money
        data["watercanuses"] = player.watercanuses
        data["exp"] = player.exp
        data["nextlvlexp"] = player.nextlvlexp
        data["level"] = player.level
        #Save time
        data["gametime"] = int(time.time())
        data["gameseed"] = self.getgameseed()
        #save tiles
        data["fields"] = []

        #fill tiles
        for farmid in xrange(self.getfarmcount()):
            farm = self.getfarm(farmid)
            data["fields"].append({"tiles":[]})
            for ftt in farm.farmtiles.keys():
                ft = farm.farmtiles[ftt]
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
                    tile["object"]['to_harvest'] = bool(gameobject.to_harvest)
                    tile["object"]['harvestcount'] = gameobject.harvestcount
                #set tile
                data["fields"][farmid]["tiles"].append(tile)
        #save data
        data.save("field.json")
        return True

    def load_gamestate(self, filename, player):
        if not os.path.isfile(filename):return False
        print ("Loading game state...")
        data = DictMapper()
        data.load(filename)
        player.inventory = data["inventory"]
        player.itemscounter = data["itemscounter"]
        player.watercanuses = data.get("watercanuses", 100)
        player.exp = data.get("exp", 0.0)
        player.nextlvlexp = data.get("nextlvlexp", 100.0)
        player.money = int(data.get("money", 1))
        player.level = int(data.get("level", 1))
        #loda game time
        self.seconds_to_update = int(time.time()) - data.get("gametime", \
                                                            int(time.time()))
        seed = data.get("gameseed", int(time.time()))
        self.setgameseed(seed)

        #Migrate old farm
        if "fields" not in data.keys():
            data["fields"] = []
            data['fields'].append({})
            data['fields'][0]["tiles"] = data["tiles"]
        #load tiles
        for farmid in xrange(len(data["fields"])):
            farm = self.getfarm(farmid)
            if farm is None:farm = self.addfarm()
            #Restore tiles
            for tile in data["fields"][farmid]["tiles"]:
                px = tile["px"]
                py = tile["py"]
                #Avoid null objects
                if not tile["object"]:continue

                #Restore seed or object
                if tile["object"]["type"] == "seed":
                    objectdata = tile["object"]
                    newobject = Seed()

                    newobject.id = objectdata["id"]
                    newobject.type = objectdata["type"]

                    newobject.to_harvest = objectdata["to_harvest"]
                    newobject.growing = objectdata["growing"]
                    newobject.growendtime = objectdata["growendtime"]
                    newobject.growstarttime = objectdata["growstarttime"]

                    farmtile = FarmTile(newobject)
                    farmtile["water"] = tile["water"]

                    #Apply global object data
                    newobject.apply_dict(objects[newobject.id])

                    #Restore harvest count
                    newobject.harvestcount = objectdata.get("harvestcount", 1)
                    newobject.requiredlevel = objectdata.get("requiredlevel", 1)
                else:
                    newobject = FarmObject()

                    newobject.id = tile["object"]["id"]
                    newobject.type = tile["object"]["type"]
                    #apply dict
                    newobject.apply_dict(objects[newobject.id])
                    farmtile = FarmTile(newobject)
                #set farmtile
                farm.set_farmtile(px, py, farmtile)
        #return
        return True
