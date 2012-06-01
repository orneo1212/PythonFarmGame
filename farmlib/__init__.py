import os
import pygame

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

rules = DictMapper()
rules.load(os.path.join("data", "rules.json"))

images = DictMapper()
images.load(os.path.join("data", "images.json"))

__VERSION__ = rules["VERSION"]

from pluginsystem import basePluginSystem as PluginSystem

pygame.init()
clickfilename = os.path.join(os.path.join("data", "sounds"), "click.wav")
clicksound = pygame.mixer.Sound(clickfilename)
