'''
Created on 27-05-2012

@author: orneo1212
'''
import os
import time

import pygame

import farmlib

from farmlib import __VERSION__
from farmlib.farmfield import FarmField
from farmlib.imageloader import ImageLoader
from farmlib.player import Player
from farmlib.timer import Timer
from farmlib.expbar import ExpBar
from farmlib.renderfunctions import render_field, render_rain
from farmlib.renderfunctions import render_seed_notify
from farmlib.renderfunctions import draw_selected_seed
from farmlib.renderfunctions import draw_tools

from farmlib.farmobject import objects
from farmlib.marketwindow import MarketWindow
from farmlib.inventorywindow import InventoryWindow
from farmlib import PluginSystem
from farmlib.coreplugin import CorePlugin

from pygameui import Label, Button, Window, Image

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

        self.farm = FarmField()
        self.eventstimer = Timer()

        self.groups = [None] # view groups
        self.images = ImageLoader(imagesdata)
        self.notifyfont = pygame.font.Font("dejavusansmono.ttf", 12)
        self.font2 = pygame.font.Font("dejavusansmono.ttf", 18)

        #Install plugins
        self.coreplugin = PluginSystem.installPlugin(CorePlugin)
        self.coreplugin.gamewindow = self

        #player
        self.player = Player()

        #background image
        bgimg = Image(self.images['background'], (0, 0))
        self.addwidget(bgimg)

        #Market button
        marketbutton = Button("Market", (710, 0), labelsize = 25, \
                             color = (253, 208, 23))
        marketbutton.connect("clicked", lambda x:self.sellwindow.togglevisible())
        self.addwidget(marketbutton)

        #create marketwindow
        self.sellwindow = MarketWindow((400, 400), self.images, self.player)

        #Create inventory window
        self.inventorywindow = InventoryWindow(self.images, self.player)

        #Create expbar
        self.expbar = ExpBar(self.player)
        self.addwidget(self.expbar)

        #labels
        self.moneylabel = Label("", (400, 5), align = "center")
        self.addwidget(self.moneylabel)

        versionlabel = Label("v. " + __VERSION__, (5, 580))
        self.addwidget(versionlabel)

        self.running = False
        self.farmoffset = (212, 50)
        self.redrawfarmfield = True

    def update(self):
        """Update farm"""
        Window.update(self)
        self.eventstimer.tick()

        #update inventory
        self.inventorywindow.update()

        #update a farm
        modified = self.farm.update()
        if modified:
            self.regenerate_groups()

    def update_current_money(self):
        #Render current money
        text = "Money: $%s " % self.player.money
        self.moneylabel.settext(text)

    def regenerate_groups(self):
        self.inventorywindow.create_gui()
        self.update_current_money()

    def handle_farmfield_events(self, event):
        #Mouse motion
        mx, my = pygame.mouse.get_pos()

        #left mouse button
        if pygame.mouse.get_pressed()[0] == 1 and \
            self.eventstimer.tickpassed(1):

            pos = self.get_farmtile_pos_under_mouse()

            if pos:
                #Emit toolused event
                PluginSystem.emit_event(
                                        "toolused",
                                        farm = self.farm,
                                        player = self.player,
                                        toolname = self.player.selectedtool,
                                        position = pos)

            if self.player.selectedtool == 'plant' and pos:
                done = False
                #TODO: Create object insted seed if placed
                #Plant seed if user have it and its empty field
                selecteditem = self.player.selecteditem
                newseed = self.player.create_new_seed_by_id(selecteditem)
                if not newseed:
                    self.player.selecteditem = None
                #check player level
                elif self.player.level >= newseed.requiredlevel:
                    done = self.farm.plant(pos[0], pos[1], newseed)
                    if done:self.player.remove_item(newseed.id)
                #regenerate sprites
                if done:self.regenerate_groups()

        #events for inventory
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #events for tools
            for tool in TOOLS:
                index = TOOLS.index(tool)
                rect = (10 + 50 * index, 10, 48, 48)
                if pygame.Rect(rect).collidepoint((mx, my)):
                    farmlib.clicksound.play()
                    self.player.selectedtool = tool
                    #regenerate sprites
                    self.regenerate_groups()

    def active_game_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.player.selectedtool = "harvest"
            if event.key == pygame.K_2:
                self.player.selectedtool = "plant"
            if event.key == pygame.K_3:
                self.player.selectedtool = "watering"
            if event.key == pygame.K_4:
                self.player.selectedtool = "shovel"
            if event.key == pygame.K_5:
                self.player.selectedtool = "pickaxe"
            if event.key == pygame.K_6:
                self.player.selectedtool = "axe"

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
                    else:
                        self.go_to_main_menu()
                #Events only for active game
                if not self.sellwindow.visible:
                    self.active_game_events(event)
                #
                if event.key == pygame.K_s:
                    self.sellwindow.togglevisible()
                if event.key == pygame.K_i:
                    self.inventorywindow.togglevisible()
            #Handle farmfield events
            if not self.sellwindow.visible:
                self.handle_farmfield_events(event)


    def redraw(self, screen):
        """Redraw screen"""
        Window.draw(self, screen)

        #Draw gamewindow
        self.draw(screen)

        #Draw farmfield
        render_field(screen, self.images, self.farm, self.farmoffset)

        #draw rain
        if self.farm.raining:
            render_rain(screen)

        drawnearcursor = not self.sellwindow.visible
        #Draw tools and selected tool rectangle
        draw_tools(screen,
                   self.player.selectedtool,
                   self.player.selecteditem,
                   self.images,
                   drawnearcursor = drawnearcursor)

        #draw watercanuses
        uses = Label("", (110 + 2, 10 + 2), color = (255, 240, 240))
        uses.settext(str(self.player.watercanuses))
        uses.draw(screen)

        if not self.sellwindow.visible:

            mx, my = pygame.mouse.get_pos()

            #draw inventory
            self.inventorywindow.draw(screen)

            #draw notify window if mouse under seed
            pos = self.get_farmtile_pos_under_mouse()
            if pos:
                farmtile = self.farm.get_farmtile(pos[0], pos[1])
                farmobject = farmtile['object']
                render_seed_notify(screen, self.notifyfont,
                                   mx + 5, my + 5,
                                   farmobject, farmtile, self.images
                                  )
        #draw selected seed
        if self.player.selecteditem != None:
            draw_selected_seed(screen, self.player.selecteditem, self.images)

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

    def start_new_game(self):
        self.farm.generate_random_stones()
        self.farm.generate_random_planks()

    def go_to_main_menu(self):
        self.deinit()
        from farmlib.menuwindow import MenuWindow
        self.parent.set_active_screen(MenuWindow())
        self.parent.inmenu = True
        self.parent.ingame = False

    def init(self):
        self.running = True
        #Load game
        result = self.farm.load_farmfield('field.json', self.player)
        if not result:
            self.start_new_game()
            print "No save game found. Starting new one"
        #render game field
        self.regenerate_groups()

    def deinit(self):
        #stop game
        self.running = False
        self.farm.save_farmfield('field.json', self.player)
