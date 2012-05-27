'''
Created on 27-05-2012

@author: orneo1212
'''
import pygame

from farmlib.gui import Label, Button, Container, Image

class MenuWindow(Container):
    def __init__(self):
        self.parent = None
        Container.__init__(self, (800, 600), (0, 0))
        self.running = True

        #background
        bgimage = pygame.Surface((800, 600))
        bgimage.fill((80, 80, 80))
        bg = Image(bgimage, (0, 0))
        self.addwidget(bg)

        #Game label
        self.gamelabel = Label("Farm game", (400, 10), align = "center",
                                  color = (0, 0, 255), size = 48)
        self.addwidget(self.gamelabel)

        #start button
        self.startbutton = Button("Start game / Continue", (320, 90),
                                  color = (255, 255, 200))
        self.startbutton.connect("clicked", self.on_startgame)
        self.addwidget(self.startbutton)

        #Quit button
        self.quitbutton = Button("Quit", (320, 110), color = (255, 0, 0))
        self.quitbutton.connect("clicked", self.on_quit)
        self.addwidget(self.quitbutton)

    def on_quit(self, widget, **data):
        self.running = False

    def on_startgame(self, widget, **data):
        self.parent.set_active_screen(self.parent.gamescreen)
        self.parent.gamescreen.init()
        self.parent.inmenu = False
        self.parent.ingame = True
        self.running = False

    def events(self):
        for event in pygame.event.get():
            #poll event to window
            self.poll_event(event)
            self.repaint()
            #
            if event.type == pygame.QUIT:
                self.running = False
