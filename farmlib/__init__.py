import os
import pygame

import imageloader
import player

from dictmapper import DictMapper


#SETTINGS

rules = DictMapper()
rules.load(os.path.join("data", "rules.json"))

images = DictMapper()
images.load(os.path.join("data", "images.json"))

__VERSION__ = rules["VERSION"]

#init plugin system
from pluginsystem import basePluginSystem as PluginSystem

pygame.font.init()
pygame.mixer.init()

clickfilename = os.path.join(os.path.join("data", "sounds"), "click.wav")
clicksound = pygame.mixer.Sound(clickfilename)
