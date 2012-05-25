from farmlib.seed import Seed, seeds

class Player:
    def __init__(self):
        self.inventory = [0, 1, 2, 3]
        self.itemscounter = {'0':1, '1':1, '2':1, '3':1}
        self.money = 0

    def update(self):
        #create dict key if not exist in itemscounter
        for i in self.inventory:
            if not self.itemscounter.has_key(str(i)):
                self.itemscounter[str(i)] = 0

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


    def create_new_seed_by_id(self, itemid):
        """Create new seed from seeds dictionary"""

        if self.item_in_inventory(itemid):
            self.remove_item(itemid)
            seed = Seed()
            seed.apply_dict(seeds[itemid])
            return seed
        #There no seed in inventory
        return False

    def event_harvest(self, seedharvested):
        #self.money += seedharvested.growtime / 120
        pass