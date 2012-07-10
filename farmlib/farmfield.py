import os
import random
import time
import base64

import farmlib
from farmlib.seed import Seed
from farmlib.dictmapper import DictMapper
from farmlib.farmobject import FarmObject, objects

class FarmField:

    def __init__(self):
        """ Init FarmField"""

        self.farmtiles = {}
        self.raining = False
        self.raintime = time.time()
        self.last_checksum = ""

    def get_farm_checksum(self):
        checksum = base64.b64encode(str(self.farmtiles))
        return checksum

    def ismodified(self):
        """Return true when farmfield is modified (based on checksum)"""
        checksum = self.get_farm_checksum()
        if checksum != self.last_checksum:
            self.last_checksum = checksum
            return True
        else:return False


    def count_anthills(self):
        anthills = 0
        for f in self.farmtiles.values():
            if f["object"] and f["object"].id == 1:
                anthills += 1
        return anthills

    def get_farmtile(self, posx, posy):
        """Get farmtile from given position"""

        arg = str(posx) + 'x' + str(posy)
        if self.farmtiles.has_key(arg):
            return self.farmtiles[arg]

        else:
            self.farmtiles[arg] = self.newfarmtile()
            return self.farmtiles[arg]

    def get_farmobject(self, posx, posy):
        """Get farmobject from given position"""
        farmtile = self.get_farmtile(posx, posy)
        if not farmtile:return None
        else:return farmtile["object"]

    def set_farmobject(self, posx, posy, farmobject):
        """Set farmobject at given position"""
        farmtile = self.get_farmtile(posx, posy)
        if farmtile:
            farmtile["object"] = farmobject

    def get_farmtile_position(self, farmtile):
        """
            Return farmtile position by spliting farmtile key in
            farmtiles dict.
        """
        for ft in self.farmtiles.keys():
            if self.farmtiles[ft] == farmtile:
                px = int(ft.split('x')[0])
                py = int(ft.split('x')[1])
                return (px, py)

    def set_farmtile(self, posx, posy, farmtile):
        """Set farmtile at given position"""

        arg = str(posx) + 'x' + str(posy)
        self.farmtiles[arg] = farmtile

    def newfarmtile(self, farmobject = None):
        """return new farmtile with keys set"""
        ft = {"water":0, "object":farmobject}
        return ft

    def plant(self, posx, posy, fobject):
        """Plant a seed on the given farmtile position"""

        farmobject = self.get_farmobject(posx, posy)
        if not farmobject:
            #Set object
            self.set_farmobject(posx, posy, fobject)
            #start growing if object is seed
            if fobject.type == "seed":
                fobject.start_grow()
            return True
        else:
            return False #  error there something on that position

    def harvest(self, posx, posy, player):
        """Harvest growed seed from farmtile"""

        farmtile = self.get_farmtile(posx, posy)
        if not farmtile["object"]:return False

        if not farmtile["object"].type == "seed":return False

        if not farmtile['object'].growing and \
            farmtile['object'].to_harvest:
            #harvest seeds
            player.event_harvest(farmtile['object'])
            for i in xrange(farmtile['object'].growquantity):
                #
                itemid = farmtile['object'].id
                if itemid not in player.inventory:
                    player.inventory.append(itemid)
                    player.itemscounter[str(itemid)] = 1
                else:
                    player.itemscounter[str(itemid)] += 1

            #Remove seed or start grow again when multi harvest seed
            harvestcount = getattr(farmtile["object"], "harvestcount", 1)
            if harvestcount > 1:
                farmtile["object"].harvestcount -= 1
                farmtile["object"].to_harvest = False
                farmtile["object"].start_grow()
            else:
                farmtile['object'] = None
                farmtile['water'] = 0
            return True

    def wilt_plant(self, posx, posy):
        fobject = FarmObject()
        fobject.id = 8 #  Wilted plant
        fobject.apply_dict(objects[fobject.id])
        farmtile = self.newfarmtile(fobject)
        self.set_farmtile(posx, posy, farmtile)
        return True

    def removewilted(self, posx, posy, player):
        self.remove(posx, posy, player)

    def remove(self, posx, posy, player):
        self.set_farmtile(posx, posy, self.newfarmtile())

    def water(self, posx, posy):
        """Watering a farm tile"""

        farmtile = self.get_farmtile(posx, posy)
        if not farmtile["object"] or not farmtile["object"].type == "seed":
            return False
        #only water dry ground
        if farmtile['water'] < 30:
            farmtile['water'] = 100
            return True
        else:return False

    def create_random_anthill(self, farmtile):
        fobject = FarmObject()
        fobject.id = 7 #  Anthill
        fobject.apply_dict(objects[fobject.id])
        farmtile["object"] = fobject
        return fobject

    def generate_random_stones(self):
        for x in xrange(random.randint(10, 15)):
            xx = random.randint(0, 11)
            yy = random.randint(0, 11)
            fobject = FarmObject()
            fobject.id = 6 #  Stone
            fobject.apply_dict(objects[fobject.id])
            farmtile = self.newfarmtile(fobject)
            self.set_farmtile(xx, yy, farmtile)

    def generate_random_planks(self):
        for x in xrange(random.randint(10, 15)):
            xx = random.randint(0, 11)
            yy = random.randint(0, 11)
            fobject = FarmObject()
            fobject.id = 9 #  Plank
            fobject.apply_dict(objects[fobject.id])
            farmtile = self.newfarmtile(fobject)
            self.set_farmtile(xx, yy, farmtile)

    def check_wilted(self, farmtile):
        if not farmtile['object']:return False

        fobject = farmtile['object']
        if fobject.type != "seed":return False

        wiltime = farmlib.rules["WILT_TIME_HOURS"]
        if fobject.to_harvest:
            if time.time() > fobject.growendtime + wiltime * 3600:

                #get position
                position = self.get_farmtile_position(farmtile)
                if not position:return False
                posx, posy = position

                self.wilt_plant(posx, posy)
                return True
        return False

    #UPDATE
    def update(self):
        """update a farmtiles"""

        modified = False

        #Toggle rain
        if self.raintime + farmlib.rules["RAIN_INTERVAL_SECS"] < \
            time.time():
            #Toggle rain
            self.raintime = time.time()
            self.raining = not self.raining

        #update each farmtile
        for farmtile in self.farmtiles.values():

            #Update objects
            if farmtile['object']:
                ret = farmtile['object'].update(farmtile)
                if ret:modified = True
                ret = self.check_wilted(farmtile)
                if ret:modified = True

                #Drying
                if int(time.time()) % 5 == 0:
                    farmtile["water"] -= 0.03
                    if farmtile["water"] < 0:farmtile["water"] = 0
            else:
                #Create anthills
                chance = random.randint(0, 10000)
                maxanthills = farmlib.rules["MAX_ANTHILLS"]
                if chance == 1 and int(time.time()) % 600 == 0\
                    and self.count_anthills() < maxanthills:
                    self.create_random_anthill(farmtile)
                    return True
        return modified

    def save_farmfield(self, filename, player):
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
        #save tiles
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
                tile["object"]['to_harvest'] = bool(gameobject.to_harvest)
                tile["object"]['harvestcount'] = gameobject.harvestcount
            #set tile
            data["tiles"].append(tile)
        #save data
        data.save("field.json")
        return True

    def load_farmfield(self, filename, player):
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

        #load tiles
        for tile in data["tiles"]:
            px = tile["px"]
            py = tile["py"]
            #Port from old saves
            if "seed" in tile:
                tile["object"] = tile["seed"]
                tile["object"]["type"] = "seed"
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

                farmtile = self.newfarmtile(newobject)
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
                farmtile = self.newfarmtile(newobject)
            #set farmtile
            self.set_farmtile(px, py, farmtile)
        #return
        return True
