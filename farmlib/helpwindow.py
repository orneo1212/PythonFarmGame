'''
Created on 24-05-2012

@author: orneo1212
'''
from pygameui import Label, Window

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
        messages = [
             "TIPS:",
            "* Plant seeds and harvest to get money",
            "* There is a chance to lost plant when its ready",
            "* You can DESTROY plant using shovel.",
            "",
            "KEYS:",
            "S - Open/Close market  I - Open/Close inventory",
            "Z/X - Go to previous/next farm",
            "M - Mute/Unmute sounds",
            ]

        label = Label("GAME HELP", (250, 5), size = 18,
                           color = (255, 255, 0), align = "center")
        self.addwidget(label)

        fontsize = 12
        index = 0
        for msg in messages:
            label = Label(msg, \
                (10, 25 + (fontsize + 2) * index), size = fontsize,
                color = (255, 240, 240), align = "left")
            self.addwidget(label)
            index += 1

