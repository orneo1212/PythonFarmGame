import time

class Seed:

    def __init__(self):
        """Init new seed"""

        self.name="New Seed"
        self.description="New seed description"
        self.id=0

        self.growtime=60 # grow time in seconds
        self.growstarttime=0 # when grow was been started
        self.growquantity=2 #  how many new seeds you got when seed fully grow

        self.growendtime=0
        self.growtimeremaining=0
        self.growing=False

        self.to_harvest=False

        self.price=0

    def update(self, farmtile):
        """update a seed"""

        self.growtimeremaining=int(self.growendtime-time.time())
        if self.growtimeremaining<0:self.growtimeremaining=0

        #calculate remaining time in hours, minutes and seconds
        remain=self.growtimeremaining
        remH=remain/3600
        remain-=remH*3600
        remM=remain/60
        remain-=remM*60
        remS=remain
        #change to string
        if remH<10:remH="0"+str(remH)
        if remM<10:remM="0"+str(remM)
        if remS<10:remS="0"+str(remS)

        self.remainstring="%sh %sm %ss" % (remH,remM,remS)

        if self.growing:

            #check for grow complete
            if self.growtimeremaining==0:
                self.growing=False
                self.to_harvest=True

    def start_grow(self):
        """Start seed growing"""

        self.growing=True
        self.growstarttime=int(time.time())
        self.growendtime=self.growstarttime+self.growtime

    def apply_dict(self,dictionary):
        """apply dictionary to object"""

        self.__dict__.update(dictionary)
