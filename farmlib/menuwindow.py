'''
Created on 27-05-2012

@author: orneo1212
'''
import os

import pygame

from pygameui import Label, Button, Container, Image
from farmlib.gamewindow import GameWindow

class MenuWindow(Container):
    def __init__(self):
        self.parent = None
        Container.__init__(self, (800, 600), (0, 0))
        self.running = True

        self.menupos = 0
        self.maxmenupos = 1

        #background
        imgpath = os.path.join("images", "gui", "mainmenubg.png")
        bgimage = pygame.image.load(imgpath).convert_alpha()
        bg = Image(bgimage, (0, 0))
        self.addwidget(bg)

        #start button
        self.menucursor = Label("-> ", (230, 120),
                                  color = (255, 255, 0), size = 20)
        self.addwidget(self.menucursor)

        #start button
        self.startbutton = Button("Start game / Continue", (270, 120),
                                  color = (255, 255, 200), labelsize = 20)
        self.startbutton.connect("clicked", self.on_startgame)
        self.addwidget(self.startbutton)

        #Quit button
        self.quitbutton = Button("Quit", (270, 160),
                                color = (255, 0, 0),
                                labelsize = 20)
        self.quitbutton.connect("clicked", self.on_quit)
        self.addwidget(self.quitbutton)

        #Show window
        self.show()

    def on_quit(self, widget, **data):
        self.running = False

    def on_startgame(self, widget, **data):
        self.startbutton.settext("Loading...")
        self.parent.gamescreen = GameWindow()
        self.parent.set_active_screen(self.parent.gamescreen)
        self.parent.gamescreen.init()
        self.parent.inmenu = False
        self.parent.ingame = True
        self.running = False

    def redraw(self, surface):
        Container.draw(self, surface)

    def update_menu_cursor(self):
        if self.menupos < 0:self.menupos = 0
        if self.menupos > self.maxmenupos:self.menupos = self.maxmenupos
        newpos = [230, 120 + 40 * self.menupos]
        self.menucursor.position = newpos
        self.repaint()

    def events(self):
        for event in pygame.event.get():
            #poll event to window
            self.poll_event(event)
            #
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.menupos += 1
                    self.update_menu_cursor()
                if event.key == pygame.K_UP:
                    self.menupos -= 1
                    self.update_menu_cursor()
                if event.key == pygame.K_RETURN:
                    if self.menupos == 0:self.on_startgame(None)
                    if self.menupos == 1:self.running = False
