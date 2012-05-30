__VERSION__ = "0.4.2"
import os

import farmobject
import seed
import farmfield
import imageloader
import inventory
import player

#GUI
import gui

from dictmapper import DictMapper


#SETTINGS
STONE_REMOVE_COST = 100
ANTHILL_REMOVE_COST = 300


rules = DictMapper()
rules.load(os.path.join("data", "rules.json"))

images = DictMapper()
images.load(os.path.join("data", "images.json"))
