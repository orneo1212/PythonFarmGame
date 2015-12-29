from __future__ import absolute_import

import os
import pygame

from farmlib.dictmapper import DictMapper
from farmlib.pluginsystem import base_plugin_system as PluginSystem


# SETTINGS

rules = DictMapper()
rules.load(os.path.join("data", "rules.json"))

images = DictMapper()
images.load(os.path.join("data", "images.json"))

__VERSION__ = rules["VERSION"]

# init plugin system

pygame.font.init()
pygame.mixer.init()

filename = os.path.join("data", "sounds", "click.wav")
if os.path.isfile(filename):
    clickfilename = filename
elif os.path.isfile(os.path.join('..', filename)):
    clickfilename = os.path.join('..', filename)
else:
    # handle error in a way that doesn't make sphinx crash
    print("ERROR: No such file: '{}'".format(filename))

clicksound = pygame.mixer.Sound(clickfilename)
