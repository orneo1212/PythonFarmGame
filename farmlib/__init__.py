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
__VERSION__ = "0.4.4"

rules = DictMapper()
rules.load(os.path.join("data", "rules.json"))

images = DictMapper()
images.load(os.path.join("data", "images.json"))
