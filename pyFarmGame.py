#!/usr/bin/env python
#-*- coding:utf-8 -*-
import pygame

from farmlib.farmfield import FarmField
from farmlib.imageloader import ImageLoader
from farmlib.inventory import PygameInventory
from farmlib.player import Player
from farmlib.window import Window
from farmlib.widgetlabel import Label

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
    'wateringcan':'images/wateringcan.png',
    'inventory':'images/inventory.png',
    }

class FarmGamePygame:
    def __init__(self):
        """Init game"""
        self.screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF)
        self.farm = FarmField()
        self.timer = pygame.time.Clock()

        self.groups = [pygame.sprite.OrderedUpdates()] # view groups
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
        pygame.display.set_caption("PyFarmGame")

        self.running = True
        self.farmoffset = (212, 50)

    def update(self):
        """Update farm"""

        self.inventory.update()

        #update a farm
        modified = self.farm.update()
        if modified:self.generate_field_sprites()

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
                    self.generate_field_sprites()

                if self.currenttool == 'watering' and pos:
                    self.farm.water(pos[0], pos[1])
                    #regenerate sprites
                    self.generate_field_sprites()

            #there no seed under mouse
            else:
                if self.currenttool == 'plant' and pos:
                    self.farm.plant(pos[0], pos[1],
                        self.player.create_new_seed_by_id(self.currentseed)
                        )
                    #regenerate sprites
                    self.generate_field_sprites()

            #events for inventory
            index = self.inventory.get_index_inventory_under_mouse()
            if index:
                itemid = index[1] * self.inventory.inventorysize[0] + index[0]
                if itemid < len(self.player.inventory):
                    self.currentseed = self.player.inventory[itemid]
                    self.currenttool = 'plant'
                    #regenerate sprites
                    self.generate_field_sprites()

            #events for tools
            if pygame.Rect((10, 10, 48, 48)).collidepoint((mx, my)):
                self.currenttool = 'harvest'
                #regenerate sprites
                self.generate_field_sprites()
            if pygame.Rect((60, 10, 48, 48)).collidepoint((mx, my)):
                self.currenttool = 'plant'
                #regenerate sprites
                self.generate_field_sprites()
            if pygame.Rect((110, 10, 48, 48)).collidepoint((mx, my)):
                self.currenttool = 'watering'
                #regenerate sprites
                self.generate_field_sprites()

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
                    if event.key == pygame.K_1:
                        self.currenttool = "harvest"
                    if event.key == pygame.K_2:
                        self.currenttool = "plant"
                    if event.key == pygame.K_3:
                        self.currenttool = "watering"
                #
                if event.key == pygame.K_s:
                    if self.sellwindow.visible:
                        self.sellwindow.hide()
                    else:
                        self.sellwindow.show()
            #
            if not self.sellwindow.visible:
                self.handle_farmfield_events(event)

    def generate_field_sprites(self):
        group = self.groups[0]
        group.empty()

        #background
        sprite = pygame.sprite.Sprite()
        sprite.image = self.images.loadimage('background')
        sprite.rect = (0, 0, 800, 600)
        group.add(sprite)

        #frame
        #sprite=pygame.sprite.Sprite()
        #sprite.image=self.images.loadimage('frame')
        #sprite.rect=(
        #    self.farmoffset[0]-30,
        #    self.farmoffset[1]-30,
        #    800,
        #    600
        #    )
        #group.add(sprite)

        for y in range(12):
            for x in range(12):
                farmtile = self.farm.get_farmtile(x, y)

                posx = (x - y) * 32 + self.farmoffset[0] + 150
                posy = (x + y) * 16 + self.farmoffset[1]

                #draw ground
                sprite = pygame.sprite.Sprite()
                sprite.rect = (posx, posy, 64, 32)
                if farmtile['water'] > 20:
                    sprite.image = self.images['wetground']
                else:
                    sprite.image = self.images['dryground']
                group.add(sprite)

                #draw plant or seed
                seed = farmtile['seed']

                if seed:
                    sprite = pygame.sprite.Sprite()
                    sprite.rect = (posx, posy, 64, 32)
                    if not seed.to_harvest:
                        sprite.image = self.images['seed']
                    else:
                        sprite.image = self.images['seed' + str(seed.id)]
                    #add sprite
                    group.add(sprite)

    def redraw(self, screen):
        """Redraw screen"""

        #Draw Farmfeld
        self.groups[0].draw(screen)

        #draw tools
        #SICKLE Harvest (10,10,48,48)
        #PLANT (60,10,48,48)
        screen.blit(self.images.loadimage('sickle'), (10, 10))
        screen.blit(self.images.loadimage('plant'), (60, 10))
        screen.blit(self.images.loadimage('wateringcan'), (110, 10))

        text = "Money:%s" % self.player.money
        text = self.font2.render(text, 1, (255, 255, 255))
        text.set_colorkey((255, 0, 255))
        screen.blit(text, (400 - text.get_size()[0] / 2, 5))


        if self.currenttool == 'harvest':
            pygame.draw.rect(screen, (255, 255, 255), (10, 10, 48, 48), 1)
        if self.currenttool == 'plant':
            pygame.draw.rect(screen, (255, 255, 255), (60, 10, 48, 48), 1)
        if self.currenttool == 'watering':
            pygame.draw.rect(screen, (255, 255, 255), (110, 10, 48, 48), 1)

        if not self.sellwindow.visible:
            self.inventory.draw_inventory(screen, self.player)

            mx, my = pygame.mouse.get_pos()

            #Draw current tool
            if self.currenttool == "plant":
                img = self.images.loadimage('seed' + str(self.currentseed))
            if self.currenttool == "harvest":
                img = self.images.loadimage('sickle')
            if self.currenttool == "watering":
                img = self.images.loadimage('wateringcan')
            screen.blit(img, (mx, my - 48))

            #draw notify window if mouse under seed
            pos = self.get_farmtile_pos_under_mouse()
            if pos:
                seed = self.farm.get_farmtile(pos[0], pos[1])['seed']
                if seed:
                    self.render_notify(screen, mx + 5, my + 5, seed)
            #draw inventory
            self.inventory.draw_inventory_notify(self.screen, self.player)

        #draw selected seed
        screen.blit(
            self.images.loadimage('dryground'),
            (65, 65)
            )
        screen.blit(
            self.images.loadimage('seed' + str(self.currentseed)),
            (65, 65)
            )
        #redraw sell window
        self.sellwindow.render(screen, (200, 40))
        #update screen
        pygame.display.flip()

    def render_notify(self, screenobj, posx, posy, underseed):
        """Render notification about planted seed"""

        sizex = 200
        sizey = 150
        posy += 5

        img = pygame.Surface((sizex, sizey))
        img.fill((48, 80, 80))
        pygame.draw.rect(img, (255, 255, 255), (0, 0, sizex - 1, sizey - 1), 1)

        #Draw seed
        seedimg = self.images["seed" + str(underseed.id)]
        img.blit(seedimg, (sizex / 2 - 32, 65))

        #name
        text = "" + underseed.name + ""
        text = self.notifyfont.render(text, 0, (255, 255, 0), (255, 0, 255))
        text.set_colorkey((255, 0, 255))
        img.blit(text, (sizex / 2 - text.get_size()[0] / 2, 5))

        #remaining time
        text = "Complete in: " + underseed.remainstring
        text = self.notifyfont.render(text, 0, (255, 0, 100), (255, 0, 255))
        text.set_colorkey((255, 0, 255))
        img.blit(text, (sizex / 2 - text.get_size()[0] / 2, 25))

        #Quentity
        text = "Quantity:" + str(underseed.growquantity)
        text = self.notifyfont.render(text, 0, (255, 255, 150), (255, 0, 255))
        text.set_colorkey((255, 0, 255))
        img.blit(text, (sizex / 2 - text.get_size()[0] / 2, 45))

        #ready to harvest
        if underseed.to_harvest:
            text = self.notifyfont.render("Ready to Harvest", 0, (255, 255, 255), (255, 0, 255))
            text.set_colorkey((255, 0, 255))
            img.blit(text, (sizex / 2 - text.get_size()[0] / 2, sizey - 20))

        #alpha
        img.set_alpha(128 + 64)
        if posx > (640 - sizex):posx -= sizex
        screenobj.blit(img, (posx, posy))

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

        self.generate_field_sprites()
        while self.running:
            self.events()
            self.update()
            self.redraw(self.screen)
            self.timer.tick(30)

        self.farm.save_farmfield('field.xml', self.player)

if __name__ == '__main__':
    f = FarmGamePygame()
    f.main()

