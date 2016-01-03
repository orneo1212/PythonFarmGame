from __future__ import absolute_import

import os
import random
import time
import base64

import farmlib
from farmlib.pnoise import pnoise
from farmlib.dictmapper import DictMapper

try:
    xrange
except NameError:
    xrange = range


class FarmTile(object):
    """Farm tile represent one tile on each farm"""
    def __init__(self, obj=None):
        self.water = 0.0
        self.farmobject = obj
        self.posx = -1
        self.posy = -1

    def __getitem__(self, name):
        if name == "water":
            return self.get_water()
        elif name == "object":
            return self.get_object()
        else:
            return None

    def __setitem__(self, name, value):
        if name == "water":
            self.water = value
        elif name == "object":
            self.farmobject = value
        else:
            return None

    def __repr__(self):
        return "<FarmTile: x:{0}, y:{1}, farmobject:{2}, water:{3}>"\
            .format(self.posx, self.posy, self.farmobject, self.water)

    def get_object(self):
        """get object

        :return:
        """
        return self.farmobject

    def get_water(self):
        """get water

        :return:
        """
        return self.water

    def update(self):
        """update

        :return:
        """
        # Drying
        self.water -= 0.05
        if self.water < 0:
            self.water = 0.0


class FarmField(object):
    """Represent Farm 12x12 in size each"""

    def __init__(self, gm):
        """ Init FarmField"""
        self.gamemanager = gm
        self.farmtiles = {}
        self.raining = False
        self.raintime = time.time()
        self.last_checksum = ""
        self.seconds_to_update = 0

    def __repr__(self):
        return "<FarmField: {}>".format(self.farmtiles)

    def get_farm_checksum(self):
        """calculate checksum

        :return:
        """
        try:
            dict.iteritems
        except AttributeError:
            # Python 3
            def listvalues(d):
                """listvalues Python 3

                :param d:
                :return:
                """
                return list(d.values())
        else:
            # Python 2
            def listvalues(d):
                """listvalues Python 2

                :param d:
                :return:
                """
                return d.values()

        ft = [str(x.water) + str(x.farmobject)
              for x in listvalues(self.farmtiles)]
        try:
            checksum = base64.b64encode("".join(ft))
        except TypeError:
            checksum = base64.b64encode(bytes(str("".join(ft)).encode()))
        return checksum

    def ismodified(self):
        """Return true when farmfield is modified (based on checksum)"""
        checksum = self.get_farm_checksum()
        if checksum != self.last_checksum:
            self.last_checksum = checksum
            return True
        else:
            return False

    def markmodified(self, modified=True):
        """mark modified

        :param modified:
        :return:
        """
        if modified:
            self.last_checksum = ""
        else:
            self.last_checksum = self.get_farm_checksum()

    def count_objects(self, objectid):
        """count objects

        :param objectid:
        :return:
        """
        count = 0
        for f in self.farmtiles.values():
            if f["object"] and f["object"].id == objectid:
                count += 1
        return count

    def get_farmtile(self, posx, posy):
        """Get farmtile from given position"""

        arg = str(posx) + 'x' + str(posy)
        if arg in self.farmtiles:  # .has_key(arg):
            return self.farmtiles[arg]

        else:
            self.farmtiles[arg] = FarmTile()
            return self.farmtiles[arg]

    def get_farmobject(self, posx, posy):
        """Get farmobject from given position"""
        farmtile = self.get_farmtile(posx, posy)
        if not farmtile:
            return None
        else:
            return farmtile["object"]

    def set_farmobject(self, posx, posy, farmobject):
        """Set farmobject at given position"""
        farmtile = self.get_farmtile(posx, posy)
        if farmtile:
            farmtile.posx = posx
            farmtile.posy = posy
            farmtile["object"] = farmobject

    def set_farmtile(self, posx, posy, farmtile):
        """Set farmtile at given position"""
        arg = str(posx) + 'x' + str(posy)
        farmtile.posx = posx
        farmtile.posy = posy
        self.farmtiles[arg] = farmtile

    def plant(self, posx, posy, fobject):
        """Plant/Place a seed/object on the given farmtile position
        """
        farmobject = self.get_farmobject(posx, posy)
        if not farmobject:
            # Set object
            self.set_farmobject(posx, posy, fobject)
            fobject.onplant()
            return True
        else:
            return False  # error there something on that position

    def harvest(self, posx, posy, player):
        """Harvest growed seed from farmtile
        """
        farmtile = self.get_farmtile(posx, posy)
        if not farmtile["object"]:
            return False

        if not str(type(farmtile["object"])) == "<class 'farmlib.farm.Seed'>":
            return False

        if not farmtile['object'].growing and \
                farmtile['object'].to_harvest:
            # harvest seeds
            player.event_harvest(farmtile['object'])
            for _ in xrange(farmtile['object'].growquantity):
                #
                itemid = farmtile['object'].id
                if itemid not in player.inventory:
                    player.inventory.append(itemid)
                    player.itemscounter[str(itemid)] = 1
                else:
                    player.itemscounter[str(itemid)] += 1

            # Remove seed or start grow again when multi harvest seed
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
        """wilt plant

        :param posx:
        :param posy:
        :return:
        """
        fobject = FarmObject()
        fobject.id = 8  # Wilted plant
        fobject.apply_dict(objects[fobject.id])
        farmtile = FarmTile(fobject)
        self.set_farmtile(posx, posy, farmtile)
        return True

    def removewilted(self, posx, posy):
        """remove wilted

        :param posx:
        :param posy:
        :return:
        """
        self.remove(posx, posy)

    def remove(self, posx, posy):
        """remove

        :param posx:
        :param posy:
        :return:
        """
        self.set_farmtile(posx, posy, FarmTile())

    def water(self, posx, posy, force=False):
        """Watering a farm tile"""

        farmtile = self.get_farmtile(posx, posy)
        if not farmtile["object"] or not farmtile["object"].type == "seed":
            return False
        # only water dry ground
        if farmtile['water'] < 30 or force:
            farmtile['water'] = 100
            return True
        else:
            return False

    @staticmethod
    def create_anthill():
        """create anthill

        :param self:
        :return:
        """
        fobject = FarmObject()
        fobject.id = 7  # Anthill
        fobject.apply_dict(objects[fobject.id])
        return fobject

    def generate_random_stones(self):
        """generate random stones

        :return:
        """
        for _ in xrange(random.randint(10, 15)):
            xx = random.randint(0, 11)
            yy = random.randint(0, 11)
            fobject = FarmObject()
            fobject.id = 6  # Stone
            fobject.apply_dict(objects[fobject.id])
            farmtile = FarmTile(fobject)
            self.set_farmtile(xx, yy, farmtile)

    def generate_random_planks(self):
        """generate random planks

        :return:
        """
        for _ in xrange(random.randint(10, 15)):
            xx = random.randint(0, 11)
            yy = random.randint(0, 11)
            fobject = FarmObject()
            fobject.id = 9  # Plank
            fobject.apply_dict(objects[fobject.id])
            farmtile = FarmTile(fobject)
            self.set_farmtile(xx, yy, farmtile)

    def check_wilted(self, farmtile):
        """check wilted

        :param farmtile:
        :return:
        """
        if not farmtile['object']:
            return False

        fobject = farmtile['object']
        if not isinstance(fobject, Seed):
            return False

        if (fobject.to_harvest and time.time() > fobject.growendtime +
                farmlib.rules["WILT_TIME_HOURS"] * 3600):
            # get position
            position = self.get_farmtile_position(farmtile)
            if not position:
                return False
            posx, posy = position

            self.wilt_plant(posx, posy)
            return True
        return False

    # UPDATE
    def update(self):
        """update a farmtiles"""

        modified = False

        # Toggle rain using perlin noise
        seed = self.gamemanager.getgameseed()
        nx = time.time() * (1.0 / 128.0)
        ny = 23482.8 * (1.0 / 128)
        rainnoise = pnoise(nx, ny, seed + 0.5)
        if rainnoise > 0.2:
            self.raining = True
        else:
            self.raining = False

        try:
            dict.iteritems
        except AttributeError:
            # Python 3
            def listvalues(d):
                """listvalues Python 3

                :param d:
                :return:
                """
                return list(d.values())
        else:
            # Python 2
            def listvalues(d):
                """listvalues Python 2

                :param d:
                :return:
                """
                return d.values()

        # update each farmtile
        for farmtile in listvalues(self.farmtiles):
            # Update objects
            if farmtile['object']:
                if farmtile['object'].update(farmtile):
                    modified = True
                if self.check_wilted(farmtile):
                    modified = True
                # Water nearest plants for ponds
                if farmtile.farmobject and farmtile.farmobject.id == 11:
                    px = farmtile.posx
                    py = farmtile.posy
                    self.water(px + 1, py, True)
                    self.water(px - 1, py, True)
                    self.water(px, py + 1, True)
                    self.water(px, py - 1, True)
                # update farmtile
                farmtile.update()
            else:
                # Create anthills
                chance = random.randint(0, 10000)
                if (chance == 1 and int(time.time()) % 600 == 0 and
                        self.count_objects(7) <
                        farmlib.rules["MAX_ANTHILLS"] and not modified):
                    farmtile["object"] = self.create_anthill()
                    modified = True
        return modified


class FarmObject(object):
    """Represent Each object possible to place on Farm"""

    def __init__(self):
        self.name = ""
        self.description = ""
        self.id = 0

        self.price = 0
        self.type = ""

    def __repr__(self):
        return "<FarmObject: id:{0}, name:{1}, type:{2}>".format(
                self.id, self.name, self.type)

    def apply_dict(self, dictionary):
        """apply dictionary to object"""
        if dictionary is None:
            return
        self.__dict__.update(dictionary)

    @staticmethod
    def update(farmtile):
        """update

        :return:
        """
        return False

    def onplant(self):
        """onplant

        :return:
        """
        pass


class Seed(FarmObject):
    """Represent seed farmobject"""
    def __init__(self):
        """Init new seed"""
        FarmObject.__init__(self)
        self.type = "seed"

        self.growtime = 60  # grow time in seconds
        self.growstarttime = 0  # when grow was been started
        self.growquantity = 2
        # how many new seeds you got when seed fully grow

        self.growendtime = 0
        self.growtimeremaining = 0
        self.growing = False

        self.harvestcount = 1
        self.requiredlevel = 1

        self.to_harvest = False

        # Remaining time string
        self.remainstring = ""

    def __repr__(self):
        return "<Seed(FarmObject): id:{0}, name:{1}, type:{2}," \
               " to_harvest:{3}>".format(
                self.id, self.name, self.type, self.to_harvest)

    def update_remainig_growing_time(self, waterlevel=0):
        """Lower growtime with ground is wet

        :param waterlevel:
        :return:
        """
        if waterlevel > 0:
            groundwet = float(waterlevel) / 100.0
        else:
            groundwet = 0.0
        # calculate new groundtime. Lower growtime max 10%
        tenperc = self.growtime * 0.10
        newgrowendtime = self.growendtime - int(tenperc * groundwet)
        self.growtimeremaining = int(newgrowendtime - time.time())
        if self.growtimeremaining < 0:
            self.growtimeremaining = 0

    def update(self, farmtile):
        """update a seed"""

        self.update_remainig_growing_time(farmtile['water'])

        # calculate remaining time in hours, minutes and seconds
        remain = self.growtimeremaining
        rem_hour = int(remain / 3600)
        remain -= rem_hour * 3600
        rem_minute = int(remain / 60)
        remain -= rem_minute * 60
        rem_secound = int(remain)
        # change to string
        if rem_hour < 10:
            rem_hour = "0" + str(rem_hour)
        if rem_minute < 10:
            rem_minute = "0" + str(rem_minute)
        if rem_secound < 10:
            rem_secound = "0" + str(rem_secound)

        self.remainstring = "{0!s}h {1!s}m {2!s}s".format(rem_hour,
                                                          rem_minute,
                                                          rem_secound)

        if self.growing and self.growtimeremaining == 0:
            # check for grow complete
            self.growing = False
            self.to_harvest = True
            chance = random.randint(0, 100)
            if chance <= farmlib.rules["DESTROY_CHANCE"]:
                farmtile["object"] = None
                farmtile["water"] = 0
            return True

        return False  # not updated

    def onplant(self):
        """onplant

        :return:
        """
        self.start_grow()

    def start_grow(self):
        """Start seed growing"""

        self.growing = True
        self.growstarttime = int(time.time())
        self.growendtime = self.growstarttime + self.growtime


# load objects from json file
objects = DictMapper()
objects.load(os.path.join("data", "objects.json"))
