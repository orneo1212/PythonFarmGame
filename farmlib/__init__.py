import os
import pygame

from dictmapper import DictMapper
from pluginsystem import base_plugin_system as PluginSystem


# SETTINGS

rules = DictMapper()
rules.load(os.path.join("data", "rules.json"))

images = DictMapper()
images.load(os.path.join("data", "images.json"))

__VERSION__ = rules["VERSION"]

# init plugin system

pygame.font.init()
pygame.mixer.init()

clickfilename = os.path.join(os.path.join("data", "sounds"), "click.wav")
clicksound = pygame.mixer.Sound(clickfilename)
