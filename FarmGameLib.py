import time,os
from xml.etree import ElementTree as ET

#preetyprint
def indent(elem, level=0):
    """in-place prettyprint formatter"""
    i = "\n" + level*" "*4
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + " "*4
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

#FarmField CLASS
class FarmField:

    def __init__(self):
        """ Init FarmField"""

        self.farmtiles={}

    def get_farmtile(self, posx, posy):
        """Get farmtile from given position"""

        arg=str(posx)+'x'+str(posy)
        if self.farmtiles.has_key(arg):
            return self.farmtiles[arg]
        
        else:
            self.farmtiles[arg]={'water':0,'seed':None}
            return self.farmtiles[arg]

    def set_farmtile(self, posx, posy, farmtile):
        """Set farmtile at given position"""

        arg=str(posx)+'x'+str(posy)
        self.farmtiles[arg]=farmtile

    def plant(self, posx, posy, seed):
        """Plant a seed on the given farmtile position"""
        
        farmtile=self.get_farmtile(posx, posy)
        if not farmtile['seed'] and seed:
            #plant a new seed on empty place
            farmtile['seed']=seed
            seed.start_grow()
        else:
            return 1 #  error there something on that position
    
    def harvest(self,posx, posy, inventory, itemscounter):
        """Harvest growed seed from farmtile"""
        
        farmtile=self.get_farmtile(posx, posy)
        if farmtile['seed']:
            if not farmtile['seed'].growing and farmtile['seed'].to_harvest:
                #harvest seeds
                for i in range(farmtile['seed'].growquantity):
                    itemid=farmtile['seed'].id
                    if itemid not in inventory:
                        inventory.append(itemid)
                        itemscounter[str(itemid)]+=1
                    else:
                        itemscounter[str(itemid)]+=1
                #TODO: add feature to many years seeds
                farmtile['seed']=None
                farmtile['water']=0 
                           
    def water(self, posx, posy):
        """Watering a farm tile"""
        
        farmtile=self.get_farmtile(posx, posy)
        #only one per seed 
        if farmtile['water']<100:
            farmtile['water']=100 #  min(farmtile['water']+10,100)
            farmtile['seed'].growendtime-=20*60
    
    def status(self, posx, posy):
        """Status"""
        
        farmtile=self.get_farmtile(posx,posy)
        if farmtile['seed']:
            print farmtile['seed'].name, "-", farmtile['seed'].description, "[ End in.",farmtile['seed'].remainstring,"]"
    
    #UPDATE
    def update(self):
        """update a farmtiles"""
        
        #update each farmtile
        for farmtile in self.farmtiles.values():
            if farmtile['seed']:
                farmtile['seed'].update(farmtile)
                
#SEED  CLASS           
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

