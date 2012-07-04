'''
Created on 27-05-2012

@author: orneo1212
'''
import os

from dictmapper import DictMapper

class FarmObject:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.id = 0

        self.price = 0
        self.type = ""

    def apply_dict(self, dictionary):
        """apply dictionary to object"""
        if dictionary is None:return
        self.__dict__.update(dictionary)

    def update(self, farmtile):
        return False

#load objects from json file
objects = DictMapper()
objects.load(os.path.join("data", "objects.json"))
