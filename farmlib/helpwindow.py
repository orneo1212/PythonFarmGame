'''
Created on 24-05-2012

@author: orneo1212
'''
import pygame

import farmlib

from pygameui import Label, Image, Window, Button
from farmlib.farmobject import objects

class HelpWindow(Window):
    def __init__(self, size):
        Window.__init__(self, size, (150, 40))
        #set window alpha
        self.alphavalue = 250 * 0.95
        #Create gui
        self.create_gui()

        #hide market at load
        self.hide()

    def create_gui(self):
        #Add images for seeds in market
        posx, posy = [0, 0]
        columns = (self.width / 64) - 1

        label = Label("GAME HELP", (250, 5), size = 18,
                           color = (255, 255, 0), align = "center")
        self.addwidget(label)

        label = Label("- Plant seeds and harvest to get money", \
            (250, 20), size = 15,
            color = (255, 240, 240), align = "center")
        self.addwidget(label)

        label = Label("- Plant seeds and harvest to get money", \
            (250, 20), size = 15,
            color = (255, 240, 240), align = "center")
        self.addwidget(label)

        label = Label("- There is a chance to lost plant when its ready", \
            (250, 40), size = 15,
            color = (255, 240, 240), align = "center")
        self.addwidget(label)

