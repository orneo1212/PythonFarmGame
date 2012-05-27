'''
Created on 27-05-2012

@author: orneo
'''
import random
import os

from farmlib import __VERSION__
from farmlib.farmfield import FarmField
from farmlib.imageloader import ImageLoader
from farmlib.inventory import PygameInventory
from farmlib.player import Player

from farmlib.renderfunctions import *
from farmlib.timer import Timer

from farmlib.seed import seeds
from farmlib.farmobject import objects, FarmObject

from farmlib.gui import Label, Container, Button, Window

from farmlib.marketwindow import MarketWindow

#SETTINGS
REMOVEWILTEDCOST = 10

TOOLS = ["harvest", "plant", "watering", "shovel", "pickaxe", "axe"]

imagesdata = {
    'seed':'images/seedstartgrow.png',
    'seedhalfgrow':"images/seedhalfgrow.png",
    'seedfullgrow':"images/seedfullgrow.png",
    'dryground':'images/dryground.png',
    'wetground':'images/wetground.png',
    'background':'images/background.png',
    'sickle':'images/sickle.png',
    'plant':'images/plant.png',
    'wiltedplant':'images/wiltedplant.png',
    'wateringcan':'images/wateringcan.png',
    'shovel':'images/shovel.png',
    'pickaxe':'images/pickaxe.png',
    'axe':'images/axe.png',
    'inventory':'images/inventory.png',
    'grid':'images/grid.png',
    'grid2':'images/grid2.png',
    'marketbg':'images/marketbg.png',
    }

#merge seeds images data (seed image have seeds/seed+id.png)
for seed in seeds:
    name = "seed" + str(seed['id']) + ".png"
    seedimagepath = os.path.join("images", os.path.join("seeds", name))
    imagesdata["seed" + str(seed['id'])] = seedimagepath

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
        self.notifyfont = pygame.font.Font("droidsansmono.ttf", 12)
        self.font2 = pygame.font.Font("droidsansmono.ttf", 18)

        #selections
        self.currenttool = 'harvest'
        self.currentseed = 0

        #player
        self.player = Player()
        self.inventory = PygameInventory(self.images)

        #create game window
        self.gamewindow = Container((800, 600), (0, 0))
        self.create_game_window()

        #create marketwindow
        self.sellwindow = MarketWindow((400, 400), self.images, self.player)

        #labels
        self.moneylabel = Label("", (400, 5), align = "center")
        self.versionlabel = Label("v. " + __VERSION__, (5, 580))

        self.running = True
        self.farmoffset = (212, 50)

        #regenerate groups
        self.regenerate_groups()


    def create_game_window(self):
        #close button
        closebutton = Button("Market", (710, 0), labelsize = 25, \
                             color = (253, 208, 23))
        closebutton.connect("clicked", lambda x:self.sellwindow.togglevisible())
        self.gamewindow.addwidget(closebutton)

    def update(self):
        """Update farm"""
        self.eventstimer.tick()
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
        self.lazyscreen = render_field(self.images, self.farm, self.farmoffset)

    def handle_farmfield_events(self, event):
        #Mouse motion
        mx, my = pygame.mouse.get_pos()

        #left mouse button
        if pygame.mouse.get_pressed()[0] == 1 and \
            self.eventstimer.tickpassed(1):

            farmobject = self.get_farmobject_under_cursor()
            pos = self.get_farmtile_pos_under_mouse()

            #there is a seed under mouse
            if farmobject:
                if self.currenttool == 'harvest' and pos:
                    done = self.farm.harvest(pos[0], pos[1], self.player)
                    #regenerate sprites
                    if done:self.regenerate_groups()

                if self.currenttool == 'shovel' and pos:
                    if farmobject and farmobject.type == "seed":
                        #Remove wilted
                        if farmobject.wilted and \
                                self.player.money >= REMOVEWILTEDCOST:
                            self.player.money -= REMOVEWILTEDCOST
                            self.farm.removewilted(pos[0], pos[1], self.player)
                        #remove seed when is NOT ready
                        elif not farmobject.to_harvest:
                            self.farm.remove(pos[0], pos[1], self.player)
                        #regenerate sprites
                        self.regenerate_groups()

                if self.currenttool == 'watering' and pos:
                    done = self.farm.water(pos[0], pos[1])
                    #regenerate sprites
                    if done:self.regenerate_groups()

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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            index = self.inventory.get_index_inventory_under_mouse()
            if index:
                itemid = index[1] * self.inventory.inventorysize[0] + index[0]
                if itemid < len(self.player.inventory):
                    self.currentseed = self.player.inventory[itemid]
                    self.currenttool = 'plant'
                    #regenerate sprites
                    self.regenerate_groups()

            #events for tools
            for tool in TOOLS:
                index = TOOLS.index(tool)
                rect = (10 + 50 * index, 10, 48, 48)
                if pygame.Rect(rect).collidepoint((mx, my)):
                    self.currenttool = tool
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
            if event.key == pygame.K_5:
                self.currenttool = "pickaxe"
            if event.key == pygame.K_6:
                self.currenttool = "axe"

    def events(self):
        """Events handler"""

        for event in pygame.event.get():
            #poll events to market window
            self.gamewindow.poll_event(event)
            #poll events to market window
            self.sellwindow.poll_event(event)

            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #ESC close market window or exit from game
                    if self.sellwindow.visible:
                        self.sellwindow.hide()
                    else:
                        self.running = False
                #Events only for active game
                if not self.sellwindow.visible:
                    self.active_game_events(event)
                #
                if event.key == pygame.K_s:
                    if self.sellwindow.visible:
                        self.sellwindow.hide()
                    else:
                        self.sellwindow.selecteditem = None
                        self.sellwindow.show()
            #Handle farmfield events
            if not self.sellwindow.visible:
                self.handle_farmfield_events(event)

    def redraw(self, screen):
        """Redraw screen"""

        #Draw Farmfeld
        screen.blit(self.lazyscreen, (0, 0))

        #Render current money
        text = "Money:%s" % self.player.money
        self.moneylabel.settext(text)
        self.moneylabel.redraw(screen)

        drawnearcursor = not self.sellwindow.visible
        #Draw tools and selected tool rectangle
        draw_tools(screen, self.currenttool, self.currentseed, self.images,
                   drawnearcursor = drawnearcursor)

        if not self.sellwindow.visible:

            mx, my = pygame.mouse.get_pos()

            #draw inventory
            self.inventory.draw_inventory(screen, self.player)

            #draw notify window if mouse under seed
            pos = self.get_farmtile_pos_under_mouse()
            if pos:
                farmtile = self.farm.get_farmtile(pos[0], pos[1])
                farmobject = farmtile['object']
                render_seed_notify(screen, self.notifyfont,
                                   mx + 5, my + 5,
                                   farmobject, farmtile, self.images
                                  )
            #draw inventory
            self.inventory.draw_inventory_notify(screen, self.player)
        #Draw wersion
        self.versionlabel.redraw(screen)

        #draw selected seed
        if self.currentseed != None:
            draw_selected_seed(screen, self.currentseed, self.images)

        #redraw game window
        self.gamewindow.redraw(screen)
        #redraw sell window
        self.sellwindow.redraw(screen)
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

    def get_farmobject_under_cursor(self):
        """Get Seed under mouse cursor"""

        pos = self.get_farmtile_pos_under_mouse()
        if pos:
            farmobject = self.farm.get_farmtile(pos[0], pos[1])['object']
            return farmobject

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
        for x in xrange(random.randint(10, 15)):
            xx = random.randint(0, 11)
            yy = random.randint(0, 11)
            tree = FarmObject()
            tree.id = 0
            tree.apply_dict(objects[tree.id])
            farmtile = self.farm.newfarmtile(tree)
            self.farm.set_farmtile(xx, yy, farmtile)
