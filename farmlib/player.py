from farmlib.seed import Seed, seeds

class Player:
    def __init__(self):
        self.inventory = [0, 1, 2, 3]
        self.itemscounter = {'0':1, '1':1, '2':1, '3':1}

    def update(self):
        #create dict key if not exist in itemscounter
        for i in self.inventory:
            if not self.itemscounter.has_key(str(i)):
                self.itemscounter[str(i)] = 0

    def create_new_seed_by_id(self, index):
        """Create new seed from seeds dictionary"""

        if index in self.inventory and self.itemscounter[str(index)] > 0:
            self.itemscounter[str(index)] -= 1
            #remove index from inventory if there no seeds in itemscounter
            if self.itemscounter[str(index)] == 0:
                self.inventory.remove(index)
            seed = Seed()
            seed.apply_dict(seeds[index])
            return seed
