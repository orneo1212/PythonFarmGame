'''
Created on 27-05-2012

@author: orneo1212
'''
import os

from dictmapper import DictMapper

class FarmObject:
    def __init__(self):
        self.name = ""
        self.descriptions = ""
        self.id = 0

        self.price = 0
        self.type = ""

    def apply_dict(self, dictionary):
        """apply dictionary to object"""

        self.__dict__.update(dictionary)

#load objects from json file
objects = DictMapper()
objects.load(os.path.join("data", "objects.json"))
