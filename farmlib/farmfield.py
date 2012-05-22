
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
