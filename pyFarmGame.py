#!/usr/bin/env python
#-*- coding:utf-8 -*-
import pygame
import os
from xml.etree import ElementTree as ET

from farmlib.farmfield import FarmField
from farmlib.seed import Seed

pygame.init()

class FarmGamePygame:

    def __init__(self):
        """Init game"""
        self.screen=pygame.display.set_mode((800,600),pygame.DOUBLEBUF)
        self.farm=FarmField()
        self.inventory=[0,1,2,3]
        self.itemscounter={'0':1,'1':1,'2':1,'3':1}
        self.timer=pygame.time.Clock()

        #price 10 per hour
        self.seeds=[
            {'name':"Strawberry", "description":"Grow in 2 hours.", 'growtime':3600*2, 'growquantity':4, 'price':20},
            {'name':"Onion", "description":"Grow in 1 hour.", 'growtime':3600*1, 'growquantity':4, 'price':80},
            {'name':"Bean", "description":"Grow in 8 hours.", 'growtime':3600*8, 'growquantity':5, 'price':10},
            {'name':"Carrot", "description":"Grow in 30 minutes.", 'growtime':30*60, 'growquantity':4, 'price':5},
            ]

        self.images={
            'seed0':pygame.image.load("images/strawberry.png").convert(),
            'seed1':pygame.image.load("images/onion.png").convert(),
            'seed2':pygame.image.load("images/bean.png").convert(),
            'seed3':pygame.image.load("images/carrot.png").convert(),
            'seed':pygame.image.load('images/seed.bmp').convert(),
            'dryground':pygame.image.load('images/dryground.bmp').convert(),
            'wetground':pygame.image.load('images/wetground.bmp').convert(),
            'background':pygame.image.load('images/background.png').convert(),
            'frame':pygame.image.load('images/frame.png').convert(),
            'sickle':pygame.image.load('images/sickle.png').convert(),
            'plant':pygame.image.load('images/plant.png').convert(),
            'wateringcan':pygame.image.load('images/wateringcan.png').convert(),
            }

        self.currenttool='plant'
        self.currentseed=0

        pygame.display.set_caption("PyFarmGame")
        pygame.init()

        self.prepare_images()
        self.prepare_seeds()

        self.running=True
        self.farmoffset=(212,50)
        self.inventoryoffset=(10,120)
        self.inventorysize=(5,5)

        self.notifyfont=pygame.font.Font(None,22)

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
                    self.farm.plant(pos[0], pos[1], self.create_new_seed_by_id(self.currentseed))

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

    def prepare_images(self):
        """Prepare images."""

        for im in self.images.keys():
            self.images[im].set_colorkey((255,0,255))
            self.images[im]=self.images[im].convert_alpha()

    def prepare_seeds(self):
        """Prepare seeds"""

        #make ID
        for i in range(len(self.seeds)):
            self.seeds[i]['id']=i

    def redraw(self,screen):
        """Redraw screen"""

        screen.blit(self.images['background'],(0, 0))
        screen.blit(self.images['frame'],(self.farmoffset[0]-30, self.farmoffset[1]-30))

        #draw farm
        for y in range(12):
            for x in range(12):
                farmtile=self.farm.get_farmtile(x,y)

                posx=x*32+self.farmoffset[0]
                posy=y*32+self.farmoffset[1]

                #draw ground
                if farmtile['water']==100:
                    screen.blit(self.images['wetground'],(posx, posy))
                else:
                    screen.blit(self.images['dryground'],(posx, posy))

                #draw plant or seed
                seed=farmtile['seed']
                if seed:
                    if not seed.to_harvest:screen.blit(self.images['seed'],(posx, posy))
                    else:screen.blit(self.images['seed'+str(seed.id)],(posx, posy))

                #draw grid
                pygame.draw.rect(screen,(48,80,80),(posx,posy,33,33),1)

        #draw tools
        #SICKLE Harvest (10,10,48,48)
        #PLANT (60,10,48,48)
        screen.blit(self.images['sickle'],(10,10))
        screen.blit(self.images['plant'],(60,10))
        screen.blit(self.images['wateringcan'],(110,10))
        if self.currenttool=='harvest':pygame.draw.rect(screen,(255,255,255),(10,10,48,48),1)
        if self.currenttool=='plant':pygame.draw.rect(screen,(255,255,255),(60,10,48,48),1)
        if self.currenttool=='watering':pygame.draw.rect(screen,(255,255,255),(110,10,48,48),1)

        #draw inventory
        img=pygame.Surface((5*32, 5*32))
        img.fill((48,80,80))
        img.set_alpha(128+64)
        screen.blit(img,self.inventoryoffset)
        #draw inv items
        counterx=0
        countery=0
        for item in self.inventory:
            screen.blit(self.images['seed'+str(item)],(counterx*32+self.inventoryoffset[0], countery*32+self.inventoryoffset[1]))
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
        screen.blit(self.images['seed'+str(self.currentseed)],(65,65))

        #update screen
        pygame.display.update()

    def render_notify(self,screenobj, posx, posy, underseed):
        """Render notification about planted seed"""

        sizex=200
        sizey=150

        img=pygame.Surface((sizex,150))
        img.fill((48,80,80))
        pygame.draw.rect(img, (255,255,255),(0, 0, sizex-1,sizey-1),1)

        #name
        text=self.notifyfont.render(underseed.name, 0, (255,255,0),(255,0,255))
        text.set_colorkey((255,0,255))
        img.blit(text, (sizex/2-text.get_size()[0]/2, 5))

        #remaining time
        text=self.notifyfont.render("Complete in: "+underseed.remainstring, 0, (255,0,100),(255,0,255))
        text.set_colorkey((255,0,255))
        img.blit(text, (sizex/2-text.get_size()[0]/2, 25))

        #Quentity
        text=self.notifyfont.render("Quantity:"+str(underseed.growquantity), 0, (255,255,150),(255,0,255))
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
        text=self.notifyfont.render(self.seeds[index]['name']+" x"+str(self.itemscounter[str(index)]), 0, (255,255,0),(255,0,255))
        text.set_colorkey((255,0,255))
        img.blit(text, (sizex/2-text.get_size()[0]/2, 5))

        #Descriptions
        text=self.notifyfont.render(self.seeds[index]['description'], 0, (255,0,0),(255,0,255))
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

    def save_farmfield(self, filename):
        """Save farmfield to xml file"""

        farmfield=ET.Element('FarmField',{'inventory':str(self.inventory), 'itemscounter':str(self.itemscounter)})

        for ft in self.farm.farmtiles.keys():
            posx=ft.split('x')[0]
            posy=ft.split('x')[1]

            farmtile=self.farm.farmtiles[ft]
            if not farmtile['seed']:continue

            farmtileelem=ET.Element('farmtile', {'posx':posx,'posy':posy,'water':str(farmtile['water'])})

            #store seed if exist
            if farmtile['seed']:

                seed=farmtile['seed']

                seedelem=ET.Element('seed',
                    {
                    'growstarttime':str(seed.growstarttime),
                    'growendtime':str(seed.growendtime),
                    'growing':str(int(seed.growing)),
                    'to_harvest':str(int(seed.to_harvest)),
                    'id':str(seed.id),
                    })
                farmtileelem.append(seedelem)

            farmfield.append(farmtileelem)
        #save created node to file
        ET.ElementTree(farmfield).write(filename)
        return 1

    def load_farmfield(self, filename):
        """Load farmfield from XML file"""

        if not os.path.isfile(filename):
            return 0

        rootelement=ET.parse(open(filename)).getroot()
        if rootelement.tag!="FarmField":return 1

        #load game information
        self.inventory=eval(str(rootelement.attrib['inventory']))
        self.itemscounter=eval(str(rootelement.attrib['itemscounter']))

        for elem in rootelement:
            if elem.tag=="farmtile":
                #if there is a children node (should be /seed/)
                if elem is not None:
                    #got seed
                    if elem[0].tag=="seed":
                        newseed=Seed()
                        newseed.growstarttime=int(elem[0].attrib['growstarttime'])
                        newseed.growendtime=int(elem[0].attrib['growendtime'])
                        newseed.growing=int(elem[0].attrib['growing'])
                        newseed.to_harvest=int(elem[0].attrib['to_harvest'])
                        newseed.id=int(elem[0].attrib['id'])
                        newseed.apply_dict(self.seeds[newseed.id])

                    #there no seed on the farmtile (wrong tag name)
                    else:newseed=None
                #there no seed on the farmtile
                else:newseed=None

            #restore a farmtile
            px=int(elem.attrib['posx'])
            py=int(elem.attrib['posy'])
            wa=int(elem.attrib['water'])
            newfarmtile={'water':wa, 'seed':newseed}

            self.farm.set_farmtile(px,py,newfarmtile)

        #return 1 as done
        return 1

    def create_new_seed_by_id(self,index):
        """Create new seed from seeds dictionary"""

        if index in self.inventory and self.itemscounter[str(index)]>0:
            self.itemscounter[str(index)]-=1
            #remove index from inventory if there no seeds in itemscounter
            if self.itemscounter[str(index)]==0:
                self.inventory.remove(index)
            seed=Seed()
            seed.apply_dict(self.seeds[index])
            return seed

    def main(self):
        """Main"""
        frame=0
        if frame>2000:frame=0

        result=self.load_farmfield('field.xml')
        if not result:print "No save game found. Starting new one"

        while self.running:
            self.events()
            self.update()
            self.timer.tick(30)
            if frame%2==0:self.redraw(self.screen)
            frame+=1

        self.save_farmfield('field.xml')

if __name__ == '__main__':
    f=FarmGamePygame()
    f.main()

