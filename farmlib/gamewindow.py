'''
Created on 27-05-2012

@author: orneo1212
'''
import os
import random

import pygame

import farmlib

from farmlib import __VERSION__
from farmlib.farm import objects
from farmlib.imageloader import ImageLoader
from farmlib.timer import Timer
from farmlib.expbar import ExpBar
from farmlib.renderfunctions import render_field, render_rain
from farmlib.renderfunctions import render_seed_notify
from farmlib.renderfunctions import draw_selected_seed
from farmlib.renderfunctions import draw_tools

from farmlib.marketwindow import MarketWindow
from farmlib.inventorywindow import InventoryWindow
from farmlib.helpwindow import HelpWindow
from farmlib import PluginSystem
from farmlib.coreplugin import CorePlugin

from pygameui import Label, Button, Window, Image
from farmlib.gamemanager import GameManager

REMOVEWILTEDCOST = farmlib.rules["REMOVEWILTEDCOST"]
REMOVEANTHILLCOST = farmlib.rules["REMOVEANTHILLCOST"]
REMOVESTONECOST = farmlib.rules["REMOVESTONECOST"]

TOOLS = ["harvest", "plant", "watering", "shovel", "pickaxe", "axe"]

#Images data
imagesdata = farmlib.images["imagesdata"]

#merge objects images data (objects image have objects/objects+id.png)
for gobject in objects:
    name = "object" + str(gobject['id']) + ".png"
    objectsimagepath = os.path.join("images", os.path.join("objects", name))
    imagesdata["object" + str(gobject['id'])] = objectsimagepath

class GameWindow(Window):
    def __init__(self):
        Window.__init__(self, (800, 600), (0, 0))

        self.lazyscreen = None

        #Create gamemanager
        self.gamemanager = GameManager()
        #timers
        self.eventstimer = Timer()
        self.updatetimer = Timer()

        self.images = ImageLoader(imagesdata)
        self.notifyfont = pygame.font.Font("dejavusansmono.ttf", 12)
        self.font2 = pygame.font.Font("dejavusansmono.ttf", 18)

        #Install plugins
        self.coreplugin = PluginSystem.installPlugin(CorePlugin)
        self.coreplugin.gamewindow = self


        #background image
        bgimg = Image(self.images['background'], (0, 0))
        self.addwidget(bgimg)

        #Create inventory window
        player = self.gamemanager.getplayer()
        self.inventorywindow = InventoryWindow(self.images, player)
        self.inventorywindow.hide()

        #create market window
        self.sellwindow = MarketWindow((400, 400), self.images, player, \
                                       self.gamemanager)
        self.sellwindow.gamewindow = self

        #Market button
        marketbutton = Button("", (800 - 42, 10), \
                             bgimage = self.images['marketbutton'])
        marketbutton.connect("clicked", self.toggle_market)
        self.addwidget(marketbutton)

        #Inventory button
        inventorybutton = Button("", (800 - 42, 52), \
                             bgimage = self.images['inventorybutton'])
        inventorybutton.connect("clicked", self.toggle_inventory)
        self.addwidget(inventorybutton)

        #Create help window
        self.helpwindow = HelpWindow((500, 300))

        #Create expbar
        self.expbar = ExpBar(player)
        self.addwidget(self.expbar)

        #labels
        self.moneylabel = Label("", (400, 5), align = "center")
        self.addwidget(self.moneylabel)

        #Label for version
        versionlabel = Label("v. " + __VERSION__ + " (H for help)", \
            (5, 580))
        self.addwidget(versionlabel)

        #Is game running?
        self.running = False

        #Farm position offset (to center map)
        self.farmoffset = (212, 50)

        #Temp image for farmfield redraw if not modified
        self.tempfarmimage = None

    def update(self):
        """Update farm"""
        Window.update(self)
        self.eventstimer.tick()
        self.updatetimer.tick()

        #update inventory
        self.inventorywindow.update()

        #Update game 20 times per second
        if self.updatetimer.tickpassed(20):
            self.gamemanager.update()

            #update inventory when changed
            self.update_current_money()
            if self.inventorywindow.ismodified():
                self.recreate_inventory()

    def update_current_money(self):
        player = self.gamemanager.getplayer()
        #Render current money
        text = "Money: $%s " % player.money
        self.moneylabel.settext(text)

    def recreate_inventory(self):
        self.inventorywindow.create_gui()

    def handle_farmfield_events(self, event):
        #Mouse motion
        mx, my = pygame.mouse.get_pos()

        player = self.gamemanager.getplayer()

        #left mouse button
        if pygame.mouse.get_pressed()[0] == 1:

            pos = self.get_farmtile_pos_under_mouse()

            if pos:
                #Emit toolused event
                PluginSystem.emit_event("toolused", position = pos, \
                                        gamemanager = self.gamemanager)

        #events for tools
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #events for tools
            for tool in TOOLS:
                index = TOOLS.index(tool)
                rect = (10 + 50 * index, 10, 48, 48)
                if pygame.Rect(rect).collidepoint((mx, my)):
                    farmlib.clicksound.play()
                    player.selectedtool = tool

    def toggle_market(self, widget):
        self.inventorywindow.hide()
        self.sellwindow.togglevisible()

    def toggle_inventory(self, widget):
        self.sellwindow.hide()
        self.inventorywindow.togglevisible()

    def active_game_events(self, event):
        player = self.gamemanager.getplayer()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                player.selectedtool = "harvest"
            if event.key == pygame.K_2:
                player.selectedtool = "plant"
            if event.key == pygame.K_3:
                player.selectedtool = "watering"
            if event.key == pygame.K_4:
                player.selectedtool = "shovel"
            if event.key == pygame.K_5:
                player.selectedtool = "pickaxe"
            if event.key == pygame.K_6:
                player.selectedtool = "axe"

    def events(self):
        """Events handler"""

        for event in pygame.event.get():
            #poll events to market window
            self.sellwindow.poll_event(event)
            #poll events to inventory window
            self.inventorywindow.poll_event(event)
            #gamewindow events
            self.poll_event(event)

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #ESC close market window or exit from game
                    if self.sellwindow.visible:
                        self.sellwindow.hide()
                    elif self.inventorywindow.visible:
                        self.inventorywindow.hide()
                    else:
                        self.go_to_main_menu()

                #Events only for active game
                if not self.sellwindow.visible and \
                    not self.inventorywindow.visible:

                    self.active_game_events(event)

                #Windows toggle buttons
                if event.key == pygame.K_s:
                    self.toggle_market(None)
                if event.key == pygame.K_i:
                    self.toggle_inventory(None)
                    self.recreate_inventory()
                if event.key == pygame.K_m:
                    if farmlib.clicksound.get_volume() == 0.0:
                        farmlib.clicksound.set_volume(1.0)
                    else:
                        farmlib.clicksound.set_volume(0.0)
                #help window key
                if event.key == pygame.K_h:
                    self.sellwindow.hide()
                    self.inventorywindow.hide()
                    self.helpwindow.togglevisible()
                #previous farm key
                if event.key == pygame.K_z:
                    farmcount = self.gamemanager.getfarmcount()
                    currfarmid = self.gamemanager.getcurrentfarmid()
                    if currfarmid > 0:
                        self.gamemanager.setcurrentfarm(currfarmid - 1)
                        farm = self.gamemanager.getfarm()
                        farm.markmodified()
                #next farm key
                if event.key == pygame.K_x:
                    farmcount = self.gamemanager.getfarmcount()
                    currfarmid = self.gamemanager.getcurrentfarmid()
                    if currfarmid < farmcount - 1:
                        self.gamemanager.setcurrentfarm(currfarmid + 1)
                        farm = self.gamemanager.getfarm()
                        farm.markmodified()
            #others events
            if not self.sellwindow.visible and \
                not self.inventorywindow.visible:

                self.handle_farmfield_events(event)

    def redraw(self, screen):
        """Redraw screen"""
        Window.draw(self, screen)

        #Draw gamewindow
        self.draw(screen)

        farm = self.gamemanager.getfarm()
        player = self.gamemanager.getplayer()

        #avoid temp farm image to be None
        if not self.tempfarmimage or farm.ismodified():
            #Draw farmfield
            self.tempfarmimage = render_field(screen, self.images, \
                                        farm, self.farmoffset)
        #Blit farmfield
        screen.blit(self.tempfarmimage, (0, 0))

        #draw rain
        if farm.raining and self.updatetimer.tickpassed(2):
            render_rain(screen)
            x = random.randint(0, 12)
            y = random.randint(0, 12)
            farm.water(x, y)

        drawnearcursor = not self.sellwindow.visible
        #Draw tools and selected tool rectangle
        draw_tools(screen,
                   player.selectedtool,
                   player.selecteditem,
                   self.images,
                   drawnearcursor = drawnearcursor)

        #draw watercanuses
        uses = Label("", (110 + 2, 10 + 2), color = (255, 240, 240))
        uses.settext(str(player.watercanuses))
        uses.repaint()
        uses.draw(screen)

        if not self.sellwindow.visible and \
            not self.inventorywindow.visible:

            mx, my = pygame.mouse.get_pos()

            #Draw help window
            self.helpwindow.draw(screen)

            #draw notify window if mouse under seed
            pos = self.get_farmtile_pos_under_mouse()
            if pos:
                farmtile = farm.get_farmtile(pos[0], pos[1])
                farmobject = farmtile['object']
                render_seed_notify(screen, self.notifyfont,
                                   mx + 5, my + 5,
                                   farmobject, farmtile, self.images
                                  )
        #draw selected seed
        if player.selecteditem != None:
            draw_selected_seed(screen, player.selecteditem, self.images)

        #draw inventory
        self.inventorywindow.draw(screen)
        #redraw sell window
        self.sellwindow.draw(screen)

    def get_farmtile_pos_under_mouse(self):
        """Get FarmTile position under mouse"""

        mx, my = pygame.mouse.get_pos()
        mx -= 150 + 32 + self.farmoffset[0]
        my -= self.farmoffset[1]
        xx, yy = self.screen2iso(mx, my)

        if xx < 0 or yy < 0 or xx > 11 or yy > 11:
            return None
        else:
            xx = min(12 - 1, xx)
            yy = min(12 - 1, yy)
            return (xx, yy)

    def get_farmobject_under_cursor(self):
        """Get Seed under mouse cursor"""

        pos = self.get_farmtile_pos_under_mouse()
        if pos:
            return self.farm.get_farmobject(pos[0], pos[1])

        return None

    def iso2screen(self, x, y):
        xx = (x - y) * (64 / 2)
        yy = (x + y) * (32 / 2)
        return xx, yy

    def screen2iso(self, x, y):
        x = x / 2
        xx = (y + x) / (32)
        yy = (y - x) / (32)
        return xx, yy

    def go_to_main_menu(self):
        self.deinit()
        from farmlib.menuwindow import MenuWindow
        self.parent.set_active_screen(MenuWindow())
        self.parent.inmenu = True
        self.parent.ingame = False

    def init(self):
        self.running = True
        #Load game
        result = self.gamemanager.loadgame()
        if not result:
            self.gamemanager.start_new_game()
            print ("No save game found. Starting new one")
        #Forward time to match gametime
        self.gamemanager.timeforward()


    def deinit(self):
        #stop game
        self.running = False
        self.gamemanager.savegame()
