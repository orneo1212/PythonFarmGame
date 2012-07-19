import os
import random
import time
import base64

import farmlib
from pnoise import pnoise
from dictmapper import DictMapper

class FarmTile:
    """Farm tile represent one tile on each farm"""
    def __init__(self, obj = None):
        self.water = 0.0
        self.farmobject = obj

    def __getitem__(self, name):
        if name == "water":return self.get_water()
        elif name == "object":return self.get_object()
        else:return None

    def __setitem__(self, name, value):
        if name == "water":self.water = value
        elif name == "object":self.farmobject = value
        else:return None

    def get_object(self):
        return self.farmobject

    def get_water(self):
        return self.water

    def update(self):
        #Drying
        self.water -= 0.05
        if self.water < 0:self.water = 0.0


class FarmField:
    """Represent Farm 12x12 in size each"""

    def __init__(self, gm):
        """ Init FarmField"""
        self.gamemanager = gm
        self.farmtiles = {}
        self.raining = False
        self.raintime = time.time()
        self.last_checksum = ""
        self.seconds_to_update = 0

    def get_farm_checksum(self):
        ft = [str(x.water) + str(x.farmobject) for x in self.farmtiles.values()]
        checksum = base64.b64encode("".join(ft))
        return checksum

    def ismodified(self):
        """Return true when farmfield is modified (based on checksum)"""
        checksum = self.get_farm_checksum()
        if checksum != self.last_checksum:
            self.last_checksum = checksum
            return True
        else:return False

    def markmodified(self, modified = True):
        if modified:self.last_checksum = ""
        else:self.last_checksum = self.get_farm_checksum()

    def count_objects(self, objectid):
        count = 0
        for f in self.farmtiles.values():
            if f["object"] and f["object"].id == objectid:
                count += 1
        return count

    def get_farmtile(self, posx, posy):
        """Get farmtile from given position"""

        arg = str(posx) + 'x' + str(posy)
        if self.farmtiles.has_key(arg):
            return self.farmtiles[arg]

        else:
            self.farmtiles[arg] = FarmTile()
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

    def plant(self, posx, posy, fobject):
        """Plant a seed on the given farmtile position"""

        farmobject = self.get_farmobject(posx, posy)
        if not farmobject:
            #Set object
            self.set_farmobject(posx, posy, fobject)
            fobject.onplant()
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
            for _ in xrange(farmtile['object'].growquantity):
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
        farmtile = FarmTile(fobject)
        self.set_farmtile(posx, posy, farmtile)
        return True

    def removewilted(self, posx, posy, player):
        self.remove(posx, posy, player)

    def remove(self, posx, posy, player):
        self.set_farmtile(posx, posy, FarmTile())

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
        for _ in xrange(random.randint(10, 15)):
            xx = random.randint(0, 11)
            yy = random.randint(0, 11)
            fobject = FarmObject()
            fobject.id = 6 #  Stone
            fobject.apply_dict(objects[fobject.id])
            farmtile = FarmTile(fobject)
            self.set_farmtile(xx, yy, farmtile)

    def generate_random_planks(self):
        for _ in xrange(random.randint(10, 15)):
            xx = random.randint(0, 11)
            yy = random.randint(0, 11)
            fobject = FarmObject()
            fobject.id = 9 #  Plank
            fobject.apply_dict(objects[fobject.id])
            farmtile = FarmTile(fobject)
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

        #Toggle rain using perlin noise
        seed = self.gamemanager.getgameseed()
        rainnoise = pnoise(time.time() * (1.0 / 64), 23482.8 * (1.0 / 64), seed + 0.5)
        if rainnoise > 0.0:
            self.raining = True
        else:
            self.raining = False

        #update each farmtile
        for farmtile in self.farmtiles.values():

            #Update objects
            if farmtile['object']:
                ret = farmtile['object'].update(farmtile)
                if ret:modified = True
                ret = self.check_wilted(farmtile)
                if ret:modified = True

                farmtile.update()
            else:
                #Create anthills
                chance = random.randint(0, 10000)
                maxanthills = farmlib.rules["MAX_ANTHILLS"]
                if chance == 1 and int(time.time()) % 600 == 0\
                    and self.count_objects(7) < maxanthills:
                    self.create_random_anthill(farmtile)
                    return True
        return modified


class FarmObject:
    """Represent Each object possible to place on Farm"""

    def __init__(self):
        self.name = ""
        self.description = ""
        self.id = 0

        self.price = 0
        self.type = ""

    def apply_dict(self, dictionary):
        """apply dictionary to object"""
        if dictionary is None:return
        self.__dict__.update(dictionary)

    def update(self, farmtile):
        return False

    def onplant(self):
        pass

class Seed(FarmObject):
    """Represent seed farmobject"""
    def __init__(self):
        """Init new seed"""
        FarmObject.__init__(self)
        self.type = "seed"

        self.growtime = 60 # grow time in seconds
        self.growstarttime = 0 # when grow was been started
        self.growquantity = 2 #  how many new seeds you got when seed fully grow

        self.growendtime = 0
        self.growtimeremaining = 0
        self.growing = False

        self.harvestcount = 1
        self.requiredlevel = 1

        self.to_harvest = False

        #Remaining time string
        self.remainstring = ""

    def update_remainig_growing_time(self, waterlevel = 0):
        if waterlevel > 0:
            groundwet = float(waterlevel) / 100.0
        else:
            groundwet = 0.0
        #calculate new groundtime. Lower growtime max 10%
        tenperc = self.growtime * 0.10
        newgrowendtime = self.growendtime - int(tenperc * groundwet)
        self.growtimeremaining = int(newgrowendtime - time.time())
        if self.growtimeremaining < 0:self.growtimeremaining = 0

    def update(self, farmtile):
        """update a seed"""

        self.update_remainig_growing_time(farmtile['water'])

        #calculate remaining time in hours, minutes and seconds
        remain = self.growtimeremaining
        remH = remain / 3600
        remain -= remH * 3600
        remM = remain / 60
        remain -= remM * 60
        remS = remain
        #change to string
        if remH < 10:remH = "0" + str(remH)
        if remM < 10:remM = "0" + str(remM)
        if remS < 10:remS = "0" + str(remS)

        self.remainstring = "%sh %sm %ss" % (remH, remM, remS)

        if self.growing:

            #check for grow complete
            if self.growtimeremaining == 0:
                self.growing = False
                self.to_harvest = True
                chance = random.randint(0, 100)
                if chance <= farmlib.rules["DESTROY_CHANCE"]:
                    farmtile["object"] = None
                    farmtile["water"] = 0
                return True

        return False #  not updated

    def onplant(self):
        self.start_grow()

    def start_grow(self):
        """Start seed growing"""

        self.growing = True
        self.growstarttime = int(time.time())
        self.growendtime = self.growstarttime + self.growtime


#load objects from json file
objects = DictMapper()
objects.load(os.path.join("data", "objects.json"))
