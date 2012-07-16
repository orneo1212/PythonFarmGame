import time
import random

from farm import FarmObject

class Seed(FarmObject):

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
