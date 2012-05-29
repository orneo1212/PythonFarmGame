import time
import random

from farmobject import FarmObject
DESTROY_CHANCE = 3 # from 0% to 100%

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

        self.to_harvest = False
        self.wilted = False

    def update_remainig_growing_time(self):
        self.growtimeremaining = int(self.growendtime - time.time())
        if self.growtimeremaining < 0:self.growtimeremaining = 0

    def update(self, farmtile):
        """update a seed"""

        self.update_remainig_growing_time()

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
                if chance <= DESTROY_CHANCE:
                    farmtile["object"] = None
                    farmtile["water"] = 0
                return True

        #ready to harvest
        if self.to_harvest:
            if time.time() > self.growendtime + 12 * 3600:
                self.to_harvest = False
                self.wilted = True
        return False #  not updated

    def start_grow(self):
        """Start seed growing"""

        self.growing = True
        self.growstarttime = int(time.time())
        self.growendtime = self.growstarttime + self.growtime
