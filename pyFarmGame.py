#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os

from farmlib.farmfield import FarmField
from farmlib.imageloader import ImageLoader
from farmlib.inventory import PygameInventory
from farmlib.player import Player
from farmlib.renderfunctions import *
from farmlib.timer import Timer
from farmlib.seed import seeds

from farmlib.widgetlabel import Label
from farmlib.widgetbutton import Button
from farmlib.container import Container

from farmlib.marketwindow import MarketWindow

pygame.init()
pygame.key.set_repeat(100, 100)

#SETTINGS
__VERSION__ = "0.4.2"
REMOVEWILTEDCOST = 0

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

class FarmGamePygame:
    def __init__(self):
        """Init game"""
        self.screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF)
        self.farm = FarmField()
        self.timer = pygame.time.Clock()
        self.eventstimer = Timer()

        self.groups = [None] # view groups
        self.images = ImageLoader(imagesdata)
        self.notifyfont = pygame.font.Font("droidsansmono.ttf", 12)
        self.font2 = pygame.font.Font("droidsansmono.ttf", 18)

        self.currenttool = 'harvest'
        self.currentseed = 0

        self.player = Player()
        self.inventory = PygameInventory(self.images)

        #create game window
        self.gamewindow = Container((800, 600), (0, 0))
        self.create_game_window()

        #create marketwindow
        self.sellwindow = MarketWindow((400, 400), self.images, self.player)

        self.moneylabel = Label("", (0, 0), align = "center")
        self.versionlabel = Label("v. " + __VERSION__, (5, 580))
        pygame.display.set_caption("PyFarmGame")

        self.running = True
        self.farmoffset = (212, 50)
        #regenerate groups
        self.regenerate_groups()

    def run_game(self):
        """
            Run game. Remove lock when error
        """
        try:
            self.main()
        except:
            import traceback
            traceback.print_exc()
            self.remove_game_lock()
            exit(1)

    def create_game_window(self):
        #close button
        closebutton = Button("Market", (710, 0), labelsize = 25, \
                             color = (253, 208, 23))
        closebutton.connect("clicked", lambda x:self.sellwindow.togglevisible())
        self.gamewindow.addwidget(closebutton)

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
        #left mouse button
        if pygame.mouse.get_pressed()[0] == 1 and \
            self.eventstimer.tickpassed(1):

            #Mouse motion
            mx, my = pygame.mouse.get_pos()

            seed = self.get_seed_under_cursor()
            pos = self.get_farmtile_pos_under_mouse()

            #there is a seed under mouse
            if seed:
                if self.currenttool == 'harvest' and pos:
                    self.farm.harvest(pos[0], pos[1], self.player)
                    #regenerate sprites
                    self.regenerate_groups()

                if self.currenttool == 'shovel' and pos:
                    if seed.wilted and self.player.money >= REMOVEWILTEDCOST:
                        self.player.money -= REMOVEWILTEDCOST
                        self.farm.removewilted(pos[0], pos[1], self.player)
                    #remove seed when is NOT ready
                    elif not seed.to_harvest:
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
            if pygame.Rect((160, 10, 48, 48)).collidepoint((mx, my)):
                self.currenttool = 'shovel'
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
        self.groups[0].draw(screen)

        #Render current money
        text = "Money:%s" % self.player.money
        self.moneylabel.settext(text)
        self.moneylabel.setposition((400, 5))
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
                seed = farmtile['seed']
                if seed:
                    render_seed_notify(
                                       screen,
                                       self.notifyfont,
                                       mx + 5,
                                       my + 5,
                                       seed,
                                       farmtile,
                                       self.images
                                      )
            #draw inventory
            self.inventory.draw_inventory_notify(self.screen, self.player)
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

    def check_game_lock(self):
        if os.path.isfile("game.lock"):
            raise Exception("Game is already running. If not manualy"\
                " remove game.lock file and try again")
            exit()
        else:
            open("game.lock", "w").close()

    def remove_game_lock(self):
        if os.path.isfile("game.lock"):
            os.remove("game.lock")

    def main(self):
        """Main"""
        #check for lock file
        self.check_game_lock()

        #Load game
        result = self.farm.load_farmfield('field.json', self.player)
        if not result:print "No save game found. Starting new one"

        self.regenerate_groups()

        while self.running:
            self.events()
            self.update()
            self.redraw(self.screen)
            self.eventstimer.tick()
            self.timer.tick(30)

        #Save game
        self.farm.save_farmfield('field.json', self.player)
        #remove lock
        self.remove_game_lock()

if __name__ == '__main__':
    f = FarmGamePygame()
    f.run_game()

