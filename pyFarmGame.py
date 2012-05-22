#!/usr/bin/env python
#-*- coding:utf-8 -*-
import pygame

from farmlib.seed import Seed, seeds
from farmlib.farmfield import FarmField
from farmlib.imageloader import ImageLoader

pygame.init()

imagesdata={
    'seed0':"images/strawberry.png",
    'seed1':"images/onion.png",
    'seed2':"images/bean.png",
    'seed3':"images/carrot.png",
    'seed':'images/seed.bmp',
    'dryground':'images/dryground.bmp',
    'wetground':'images/wetground.bmp',
    'background':'images/background.png',
    'frame':'images/frame.png',
    'sickle':'images/sickle.png',
    'plant':'images/plant.png',
    'wateringcan':'images/wateringcan.png',
    }

class FarmGamePygame:
    def __init__(self):
        """Init game"""
        self.screen=pygame.display.set_mode((800,600),pygame.DOUBLEBUF)
        self.farm=FarmField()
        self.inventory=[0,1,2,3]
        self.itemscounter={'0':1,'1':1,'2':1,'3':1}
        self.timer=pygame.time.Clock()

        self.groups=[pygame.sprite.OrderedUpdates()] # view groups
        self.images=ImageLoader(imagesdata)

        self.currenttool='harvest'
        self.currentseed=0

        pygame.display.set_caption("PyFarmGame")

        self.running=True
        self.farmoffset=(212,50)
        self.inventoryoffset=(10,120)
        self.inventorysize=(5,5)

        self.notifyfont=pygame.font.Font("droidsansmono.ttf",12)

    def update(self):
        """Update farm"""

        #create dict key if not exist in itemscounter
        for i in self.inventory:
            if not self.itemscounter.has_key(str(i)):
                self.itemscounter[str(i)]=0

        #update a farm
        self.farm.update()

    def events(self):
        """Events handler"""

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    self.running=False
                if event.key==pygame.K_1:
                    self.currenttool="harvest"
                if event.key==pygame.K_2:
                    self.currenttool="plant"
                if event.key==pygame.K_3:
                    self.currenttool="watering"

        #Mouse motion
        mx,my=pygame.mouse.get_pos()

        #left mouse button
        if pygame.mouse.get_pressed()[0]==1:
            seed=self.get_seed_under_cursor()
            pos=self.get_farmtile_pos_under_mouse()

            #there is a seed under mouse
            if seed:
                if self.currenttool=='harvest' and pos:
                    self.farm.harvest(pos[0], pos[1], self.inventory, self.itemscounter)

                if self.currenttool=='watering' and pos:
                    self.farm.water(pos[0], pos[1])

            #there no seed under mouse
            else:
                if self.currenttool=='plant' and pos:
                    self.farm.plant(pos[0], pos[1],
                        self.create_new_seed_by_id(self.currentseed)
                        )

            #events for inventory
            index=self.get_index_inventory_under_mouse()
            if index:
                itemid=index[1]*self.inventorysize[0]+index[0]
                if itemid<len(self.inventory):
                    self.currentseed=self.inventory[itemid]

            #events for tools
            if pygame.Rect((10,10,48,48)).collidepoint((mx,my)):
                self.currenttool='harvest'
            if pygame.Rect((60,10,48,48)).collidepoint((mx,my)):
                self.currenttool='plant'
            if pygame.Rect((110,10,48,48)).collidepoint((mx,my)):
                self.currenttool='watering'
            #regenerate sprites
            self.generate_field_sprites()

    def generate_field_sprites(self):
        group=self.groups[0]
        group.empty()

        #background
        sprite=pygame.sprite.Sprite()
        sprite.image=self.images.loadimage('background')
        sprite.rect=(0,0, 800,600)
        group.add(sprite)

        #frame
        sprite=pygame.sprite.Sprite()
        sprite.image=self.images.loadimage('frame')
        sprite.rect=(
            self.farmoffset[0]-30,
            self.farmoffset[1]-30,
            800,
            600
            )
        group.add(sprite)

        for y in range(12):
            for x in range(12):
                farmtile=self.farm.get_farmtile(x,y)

                posx=x*32+self.farmoffset[0]
                posy=y*32+self.farmoffset[1]

                #draw ground
                sprite=pygame.sprite.Sprite()
                sprite.rect=(posx, posy, 32, 32)
                if farmtile['water']>20:
                    sprite.image=self.images['wetground']
                else:
                    sprite.image=self.images['dryground']
                group.add(sprite)

                #draw plant or seed
                seed=farmtile['seed']

                if seed:
                    sprite=pygame.sprite.Sprite()
                    sprite.rect=(posx, posy, 32, 32)
                    if not seed.to_harvest:
                        sprite.image=self.images['seed']
                    else:
                        sprite.image=self.images['seed'+str(seed.id)]
                    #add sprite
                    group.add(sprite)

    def redraw(self,screen):
        """Redraw screen"""

        #Draw Farmfeld
        self.groups[0].draw(screen)

        #draw tools
        #SICKLE Harvest (10,10,48,48)
        #PLANT (60,10,48,48)
        screen.blit(self.images.loadimage('sickle'), (10,10))
        screen.blit(self.images.loadimage('plant'), (60,10))
        screen.blit(self.images.loadimage('wateringcan'), (110,10))

        if self.currenttool=='harvest':
            pygame.draw.rect(screen,(255,255,255),(10,10,48,48),1)
        if self.currenttool=='plant':
            pygame.draw.rect(screen,(255,255,255),(60,10,48,48),1)
        if self.currenttool=='watering':
            pygame.draw.rect(screen,(255,255,255),(110,10,48,48),1)

        #draw inventory
        img=pygame.Surface((5*32, 5*32))
        img.fill((48,80,80))
        img.set_alpha(128+64)
        screen.blit(img,self.inventoryoffset)
        #draw inv items
        counterx=0
        countery=0
        for item in self.inventory:
            screen.blit(self.images.loadimage('seed'+str(item)),
                (
                counterx*32+self.inventoryoffset[0],
                countery*32+self.inventoryoffset[1])
                )
            counterx+=1
            if counterx==self.inventorysize[0]:
                counterx=0
                countery+=1
            if countery==self.inventorysize[1]:break

        mx,my=pygame.mouse.get_pos()

        #draw notify window if mouse under seed
        pos=self.get_farmtile_pos_under_mouse()
        if pos:
            seed=self.farm.get_farmtile(pos[0], pos[1])['seed']
            if seed:
                self.render_notify(screen,mx,my,seed)

        #draw inventory notify window
        index=self.get_index_inventory_under_mouse()
        if index:
            itemid=index[1]*self.inventorysize[0]+index[0]
            if itemid<len(self.inventory):
                self.render_inventory_notify(screen, mx, my, self.inventory[itemid])

        #draw selected seed
        screen.blit(
            self.images.loadimage('seed'+str(self.currentseed)),
            (65,65)
            )

        #update screen
        pygame.display.flip()

    def render_notify(self,screenobj, posx, posy, underseed):
        """Render notification about planted seed"""

        sizex=200
        sizey=150

        img=pygame.Surface((sizex,sizey))
        img.fill((48,80,80))
        pygame.draw.rect(img, (255,255,255),(0, 0, sizex-1,sizey-1),1)

        #name
        text=""+underseed.name+""
        text=self.notifyfont.render(text, 0, (255,255,0),(255,0,255))
        text.set_colorkey((255,0,255))
        img.blit(text, (sizex/2-text.get_size()[0]/2, 5))

        #remaining time
        text="Complete in: "+underseed.remainstring
        text=self.notifyfont.render(text, 0, (255,0,100),(255,0,255))
        text.set_colorkey((255,0,255))
        img.blit(text, (sizex/2-text.get_size()[0]/2, 25))

        #Quentity
        text="Quantity:"+str(underseed.growquantity)
        text=self.notifyfont.render(text, 0, (255,255,150),(255,0,255))
        text.set_colorkey((255,0,255))
        img.blit(text, (sizex/2-text.get_size()[0]/2, 45))

        #ready to harvest
        if underseed.to_harvest:
            text=self.notifyfont.render("Ready to Harvest", 0, (255,255,255),(255,0,255))
            text.set_colorkey((255,0,255))
            img.blit(text, (sizex/2-text.get_size()[0]/2, sizey-20))

        #alpha
        img.set_alpha(128+64)
        if posx>(640-sizex):posx-=sizex
        screenobj.blit(img,(posx,posy))

    def render_inventory_notify(self,screenobj,posx,posy,index):
        """Render inventory notify"""

        sizex=200

        img=pygame.Surface((sizex,150))
        img.fill((48,80,80))

        #Name
        text=self.notifyfont.render(seeds[index]['name']+" x"+str(self.itemscounter[str(index)]), 0, (255,255,0),(255,0,255))
        text.set_colorkey((255,0,255))
        img.blit(text, (sizex/2-text.get_size()[0]/2, 5))

        #Descriptions
        text=self.notifyfont.render(seeds[index]['description'], 0, (255,0,0),(255,0,255))
        text.set_colorkey((255,0,255))
        img.blit(text, (sizex/2-text.get_size()[0]/2, 25))

        #alpha
        img.set_alpha(250)
        if posx>(640-sizex):posx-=sizex
        screenobj.blit(img,(posx,posy))

    def get_farmtile_pos_under_mouse(self):
        """Get FarmTile position under mouse"""

        mx,my=pygame.mouse.get_pos()
        xx=(mx-self.farmoffset[0])/32
        yy=(my-self.farmoffset[1])/32
        if xx<0 or yy<0:
            return None
        else:
            xx=min(12-1,xx)
            yy=min(12-1,yy)
            return (xx,yy)

    def get_seed_under_cursor(self):
        """Get Seed under mouse cursor"""

        pos=self.get_farmtile_pos_under_mouse()
        if pos:
            seed=self.farm.get_farmtile(pos[0],pos[1])['seed']
            return seed

        return None

    def get_index_inventory_under_mouse(self):
        """Get position of element in inventory under mouse cursor"""

        mx,my=pygame.mouse.get_pos()
        xx=(mx-self.inventoryoffset[0])/32
        yy=(my-self.inventoryoffset[1])/32

        if xx<0 or yy<0:return None
        if xx>=self.inventorysize[0]:return None
        if yy>=self.inventorysize[1]:return None
        xx=min(self.inventorysize[0]-1,xx)
        yy=min(self.inventorysize[1]-1,yy)
        return (xx,yy)

    def create_new_seed_by_id(self,index):
        """Create new seed from seeds dictionary"""

        if index in self.inventory and self.itemscounter[str(index)]>0:
            self.itemscounter[str(index)]-=1
            #remove index from inventory if there no seeds in itemscounter
            if self.itemscounter[str(index)]==0:
                self.inventory.remove(index)
            seed=Seed()
            seed.apply_dict(seeds[index])
            return seed

    def main(self):
        """Main"""

        result=self.farm.load_farmfield('field.xml')
        if not result:print "No save game found. Starting new one"

        self.generate_field_sprites()
        while self.running:
            self.events()
            self.update()
            self.redraw(self.screen)
            self.timer.tick(30)

        self.farm.save_farmfield('field.xml')

if __name__ == '__main__':
    f=FarmGamePygame()
    f.main()

