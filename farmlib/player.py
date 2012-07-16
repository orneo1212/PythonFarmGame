from farm import objects, FarmObject, Seed

class Player:
    def __init__(self):
        self.inventory = [3]
        self.itemscounter = {'3':2}
        self.money = 0
        self.watercanuses = 100
        #Skill
        self.exp = 0.0
        self.nextlvlexp = 100.0
        self.level = 1
        #selection
        self.selecteditem = None
        self.selectedtool = "harvest"

    def update(self):
        #create dict key if not exist in itemscounter
        for i in self.inventory:
            if not self.itemscounter.has_key(str(i)):
                self.itemscounter[str(i)] = 0
        #clear selection if player dont have item
        if self.selecteditem != None:
            if self.selecteditem not in self.inventory:
                self.selecteditem = None

    def item_in_inventory(self, itemid):
        if itemid is None:return False
        itemid = int(itemid)
        stritemid = str(itemid)
        if itemid in self.inventory:
            #itemid must be in itemscounter dict
            if stritemid not in self.itemscounter:
                self.itemscounter[stritemid] = 1
            return True
        else:return False

    def remove_item(self, itemid):
        itemid = int(itemid)
        stritemid = str(itemid)
        if self.item_in_inventory(itemid):
            #if there is more items in stackremove one item
            if self.itemscounter[stritemid] > 1:
                self.itemscounter[stritemid] -= 1
            #remove item
            else:
                del self.itemscounter[stritemid]
                self.inventory.remove(itemid)
            return True
        else:
            return False

    def add_item(self, itemid):
        itemid = int(itemid)
        stritemid = str(itemid)
        if self.item_in_inventory(itemid):
            self.itemscounter[stritemid] += 1
            return True
        else:
            #add item to inventory and set counter to 1
            self.inventory.append(itemid)
            self.itemscounter[stritemid] = 1


    def create_new_object_by_id(self, itemid):
        """Create new farm object from objects dictionary"""

        #If player dont have this object return False
        if not self.item_in_inventory(itemid):return False
        if objects[itemid].get("type", "object") == "seed":
            seed = Seed()
            seed.apply_dict(objects[itemid])
            return seed
        else:
            fobject = FarmObject()
            fobject.apply_dict(objects[itemid])
            return fobject



    def update_skill(self):
        self.nextlvlexp = float(self.level - 1) * 100.0 * 2.75 + 100.0
        if self.exp >= self.nextlvlexp:
            self.level += 1
            self.exp = self.exp - self.nextlvlexp

    def event_harvest(self, seedharvested):
        if seedharvested.type != "seed":return
        self.exp += seedharvested.price / 4
        self.update_skill()
