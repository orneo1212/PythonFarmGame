#!/usr/bin/env python
#-*- coding:utf-8 -*-
import pygame

from farmlib.farmfield import FarmField
from farmlib.imageloader import ImageLoader
from farmlib.inventory import PygameInventory
from farmlib.player import Player
from farmlib.window import Window
from farmlib.widgetlabel import Label
from farmlib.renderfunctions import *

pygame.init()

imagesdata = {
    'seed0':"images/strawberry.png",
    'seed1':"images/onion.png",
    'seed2':"images/bean.png",
    'seed3':"images/carrot.png",
    'seed':'images/seed.bmp',
    'dryground':'images/dryground.png',
    'wetground':'images/wetground.png',
    'background':'images/background.png',
    'frame':'images/frame.png',
    'sickle':'images/sickle.png',
    'plant':'images/plant.png',
    'wiltedplant':'images/wiltedplant.png',
    'wateringcan':'images/wateringcan.png',
    'shovel':'images/shovel.png',
    'inventory':'images/inventory.png',
    }

class FarmGamePygame:
    def __init__(self):
        """Init game"""
        self.screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF)
        self.farm = FarmField()
        self.timer = pygame.time.Clock()

        self.groups = [None] # view groups
        self.images = ImageLoader(imagesdata)
        self.notifyfont = pygame.font.Font("droidsansmono.ttf", 12)
        self.font2 = pygame.font.Font("droidsansmono.ttf", 18)

        self.currenttool = 'harvest'
        self.currentseed = 0

        self.player = Player()
        self.inventory = PygameInventory(self.images)
        self.sellwindow = Window((400, 400))
        self.sellwindow.hide()
        self.sellwindow.addwidget(Label("Market place",
                                        (200, 0),
                                        size = 18,
                                        color = (255, 255, 0),
                                        align = "center")
                                        )
        self.moneylabel = Label("", (0, 0), align = "center")
        pygame.display.set_caption("PyFarmGame")

        self.running = True
        self.farmoffset = (212, 50)

    def update(self):
        """Update farm"""
        #Clear current seed if user dont have it
        if self.currentseed != None:
            if self.currentseed not in self.player.inventory:
                self.currentseed = None
        self.inventory.update()

        #update a farm
        modified = self.farm.update()
        if modified:
            self.regenerate_groups()

    def regenerate_groups(self):
        self.groups[0] = generate_field_sprites(
                                                self.images,
                                                self.farm,
                                                self.farmoffset
                                                )

    def handle_farmfield_events(self, event):
        #Mouse motion
        mx, my = pygame.mouse.get_pos()

        #left mouse button
        if pygame.mouse.get_pressed()[0] == 1:
            seed = self.get_seed_under_cursor()
            pos = self.get_farmtile_pos_under_mouse()

            #there is a seed under mouse
            if seed:
                if self.currenttool == 'harvest' and pos:
                    self.farm.harvest(pos[0], pos[1], self.player)
                    #regenerate sprites
                    self.regenerate_groups()

                if self.currenttool == 'watering' and pos:
                    self.farm.water(pos[0], pos[1])
                    #regenerate sprites
                    self.regenerate_groups()

            #there no seed under mouse
            else:
                if self.currenttool == 'plant' and pos:
                    #Plant seed if user have it and its empty field
                    newseed = self.player.create_new_seed_by_id(self.currentseed)
                    if not newseed:
                        self.currentseed = None
                    else:
                        self.farm.plant(pos[0], pos[1], newseed)
                    #regenerate sprites
                    self.regenerate_groups()

            #events for inventory
            index = self.inventory.get_index_inventory_under_mouse()
            if index:
                itemid = index[1] * self.inventory.inventorysize[0] + index[0]
                if itemid < len(self.player.inventory):
                    self.currentseed = self.player.inventory[itemid]
                    self.currenttool = 'plant'
                    #regenerate sprites
                    self.regenerate_groups()

            #events for tools
            if pygame.Rect((10, 10, 48, 48)).collidepoint((mx, my)):
                self.currenttool = 'harvest'
                #regenerate sprites
                self.regenerate_groups()
            if pygame.Rect((60, 10, 48, 48)).collidepoint((mx, my)):
                self.currenttool = 'plant'
                #regenerate sprites
                self.regenerate_groups()
            if pygame.Rect((110, 10, 48, 48)).collidepoint((mx, my)):
                self.currenttool = 'watering'
                #regenerate sprites
                self.regenerate_groups()

    def active_game_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.currenttool = "harvest"
            if event.key == pygame.K_2:
                self.currenttool = "plant"
            if event.key == pygame.K_3:
                self.currenttool = "watering"
            if event.key == pygame.K_4:
                self.currenttool = "shovel"

    def events(self):
        """Events handler"""

        for event in pygame.event.get():
            #poll events to sell window
            self.sellwindow.poll_event(event)

            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                #Events only for active game 
                if not self.sellwindow.visible:
                    self.active_game_events(event)
                #
                if event.key == pygame.K_s:
                    if self.sellwindow.visible:
                        self.sellwindow.hide()
                    else:
                        self.sellwindow.show()
            #
            if not self.sellwindow.visible:
                self.handle_farmfield_events(event)

    def redraw(self, screen):
        """Redraw screen"""

        #Draw Farmfeld
        self.groups[0].draw(screen)

        #Render current money
        text = "Money:%s" % self.player.money
        self.moneylabel.settext(text)
        self.moneylabel.setposition((400, 5))
        self.moneylabel.redraw(screen)

        #Draw tools and selected tool rectangle
        draw_tools(screen, self.currenttool, self.currentseed, self.images)

        if not self.sellwindow.visible:
            self.inventory.draw_inventory(screen, self.player)

            mx, my = pygame.mouse.get_pos()

            #draw notify window if mouse under seed
            pos = self.get_farmtile_pos_under_mouse()
            if pos:
                seed = self.farm.get_farmtile(pos[0], pos[1])['seed']
                if seed:
                    render_seed_notify(
                                       screen,
                                       self.notifyfont,
                                       mx + 5,
                                       my + 5,
                                       seed,
                                       self.images
                                      )
            #draw inventory
            self.inventory.draw_inventory_notify(self.screen, self.player)

        if self.currentseed != None:
            draw_selected_seed(screen, self.currentseed, self.images)

        #redraw sell window
        self.sellwindow.render(screen, (200, 40))
        #update screen
        pygame.display.flip()

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

    def get_seed_under_cursor(self):
        """Get Seed under mouse cursor"""

        pos = self.get_farmtile_pos_under_mouse()
        if pos:
            seed = self.farm.get_farmtile(pos[0], pos[1])['seed']
            return seed

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

    def main(self):
        """Main"""

        result = self.farm.load_farmfield('field.xml', self.player)
        if not result:print "No save game found. Starting new one"

        self.regenerate_groups()

        while self.running:
            self.events()
            self.update()
            self.redraw(self.screen)
            self.timer.tick(30)

        self.farm.save_farmfield('field.xml', self.player)

if __name__ == '__main__':
    f = FarmGamePygame()
    f.main()

