'''
Created on 23-05-2012

@author: orneo1212
'''
import random
import pygame

def draw_tools(surface, currenttool, currentseed, imgloader,
               drawnearcursor = True):
    #Draw selection on selected tool
    if currenttool == 'harvest':
        pygame.draw.rect(surface, (255, 255, 255), (10, 10, 48, 48), 1)
    if currenttool == 'plant':
        pygame.draw.rect(surface, (255, 255, 255), (60, 10, 48, 48), 1)
    if currenttool == 'watering':
        pygame.draw.rect(surface, (255, 255, 255), (110, 10, 48, 48), 1)
    if currenttool == 'shovel':
        pygame.draw.rect(surface, (255, 255, 255), (160, 10, 48, 48), 1)
    if currenttool == 'pickaxe':
        pygame.draw.rect(surface, (255, 255, 255), (210, 10, 48, 48), 1)
    if currenttool == 'axe':
        pygame.draw.rect(surface, (255, 255, 255), (260, 10, 48, 48), 1)

    mx, my = pygame.mouse.get_pos()

    if drawnearcursor:
        img = None
        #Draw current tool
        if currenttool == "plant":
            #draw seed only when correct is selected
            if currentseed == None:
                img = None
            else:
                img = imgloader.loadimage('object' + str(currentseed))
        if currenttool == "harvest":
            img = imgloader.loadimage('sickle')
        if currenttool == "watering":
            img = imgloader.loadimage('wateringcan')
        if currenttool == "shovel":
            img = imgloader.loadimage('shovel')
        if currenttool == "pickaxe":
            img = imgloader.loadimage('pickaxe')
        if currenttool == "axe":
            img = imgloader.loadimage('axe')
        if img:
            surface.blit(img, (mx, my - 48))

    #draw tools
    #SICKLE Harvest (10,10,48,48)
    #PLANT (60,10,48,48)
    surface.blit(imgloader.loadimage('sickle'), (10, 10))
    surface.blit(imgloader.loadimage('plant'), (60, 10))
    surface.blit(imgloader.loadimage('wateringcan'), (110, 10))
    surface.blit(imgloader.loadimage('shovel'), (160, 10))
    surface.blit(imgloader.loadimage('pickaxe'), (210, 10))
    surface.blit(imgloader.loadimage('axe'), (260, 10))

def draw_seed(surface, seedid, position, imgloader):
        img = imgloader.loadimage('object' + str(seedid))
        surface.blit(img, position)

def draw_selected_seed(surface, selectedseed, imgloader):
    if  selectedseed == None:return
    #draw selected seed
    img = imgloader.loadimage('dryground')
    surface.blit(img, (65, 90))
    draw_seed(surface, selectedseed, (65, 90), imgloader)

def render_seed_notify(surface, font, posx, posy, farmobject, farmtile,
                       imgloader):
    """Render notification about farm object"""

    if farmobject is None:return

    sizex = 250
    sizey = 150
    posy += 5

    img = pygame.Surface((sizex, sizey))
    img.fill((48, 80, 80))
    pygame.draw.rect(img, (255, 255, 255), (0, 0, sizex - 1, sizey - 1), 1)

    #half of the tooltip width
    halfx = sizex / 2

    #name
    text = "" + farmobject.name + ""
    text = font.render(text, 0, (255, 255, 0), (255, 0, 255))
    text.set_colorkey((255, 0, 255))
    img.blit(text, (halfx - text.get_size()[0] / 2, 5))

    #Descriptions
    text = "" + farmobject.description + ""
    text = font.render(text, 0, (255, 240, 40), (255, 0, 255))
    text.set_colorkey((255, 0, 255))
    img.blit(text, (halfx - text.get_size()[0] / 2, 25))

    #Draw Seed info
    if farmobject.type == "seed":
        #Draw seed
        draw_seed(img, farmobject.id, (sizex / 2 - 32, 100), imgloader)
        #remaining time
        text = "Complete in: " + farmobject.remainstring
        text = font.render(text, 0, (255, 0, 100), (255, 0, 255))
        text.set_colorkey((255, 0, 255))
        img.blit(text, (halfx - text.get_size()[0] / 2, 45))

        #Quentity
        text = "Quantity: %s (%s)" % (str(farmobject.growquantity),
                                      str(farmobject.harvestcount))
        text = font.render(text, 0, (255, 255, 150), (255, 0, 255))
        text.set_colorkey((255, 0, 255))
        img.blit(text, (halfx - text.get_size()[0] / 2, 65))

        #Water
        text = "Water: " + str(int(farmtile["water"])) + " %"
        text = font.render(text, 0, (0, 128, 255), (255, 0, 255))
        text.set_colorkey((255, 0, 255))
        img.blit(text, (halfx - text.get_size()[0] / 2, 85))

        #ready to harvest
        if farmobject.to_harvest:
            text = font.render("Ready to Harvest", 0, \
                               (255, 255, 255), (255, 0, 255))
            text.set_colorkey((255, 0, 255))
            img.blit(text, (halfx - text.get_size()[0] / 2, sizey - 20))

    #alpha
    img.set_alpha(128 + 64)
    if posx > 400:posx -= sizex
    surface.blit(img, (posx, posy))

def render_rain(surface):
    for x in range(30):
        xx = random.randint(0, surface.get_size()[0])
        yy = random.randint(0, 100)
        offset = random.randint(-15, -8)
        pygame.draw.line(surface, (0, 0, 200), (xx, yy),
                         (xx + offset, yy + 15))

def render_one_field(position, screen, imgloader, farmfield, farmoffset):
    """Render one field from farm"""
    mainimg = screen
    x, y = position
    farmtile = farmfield.get_farmtile(x, y)

    posx = (x - y) * 32 + farmoffset[0] + 150
    posy = (x + y) * 16 + farmoffset[1]

    rect = (posx, posy, 64, 32)

    #draw ground
    if farmtile['water'] >= 30:
        img = imgloader['wetground']
    else:
        img = imgloader['dryground']
    mainimg.blit(img, rect)

    #draw grid
    mainimg.blit(imgloader['grid'], rect)

    #draw plant or seed
    farmobject = farmtile['object']

    #Avoid draw Null fieldobjects
    if not farmobject:return

    if farmobject.type == "seed":
        #not ready to harvest
        if not farmobject.to_harvest:
            farmobject.update_remainig_growing_time()
            #draw seeds on the ground
            if farmobject.growtimeremaining <= 30 * 60:
                img = imgloader['seedfullgrow']
            elif farmobject.growtimeremaining <= 60 * 60:
                img = imgloader['seedhalfgrow']

            else:
                img = imgloader['seed']

        #ready to harvest
        else:
            img = imgloader['object' + str(farmobject.id)]
    #Field object
    else:
        img = imgloader['object' + str(farmobject.id)]
    #Draw field image
    if img:mainimg.blit(img, rect)

def render_field(screen, imgloader, farmfield, farmoffset):
    img = pygame.surface.Surface((800, 600))
    img.set_colorkey((0, 0, 0))
    for y in range(12):
        for x in range(12):
            render_one_field((x, y), img, \
                imgloader, farmfield, farmoffset)
    return img
