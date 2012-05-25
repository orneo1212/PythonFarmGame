'''
Created on 23-05-2012

@author: orneo1212
'''
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

    mx, my = pygame.mouse.get_pos()

    if drawnearcursor:
        #Draw current tool
        if currenttool == "plant":
            #draw seed only when correct is selected
            if currentseed == None:
                img = None
            else:
                img = imgloader.loadimage('seed' + str(currentseed))
        if currenttool == "harvest":
            img = imgloader.loadimage('sickle')
        if currenttool == "watering":
            img = imgloader.loadimage('wateringcan')
        if currenttool == "shovel":
            img = imgloader.loadimage('shovel')
        if img:
            surface.blit(img, (mx, my - 48))

    #draw tools
    #SICKLE Harvest (10,10,48,48)
    #PLANT (60,10,48,48)
    surface.blit(imgloader.loadimage('sickle'), (10, 10))
    surface.blit(imgloader.loadimage('plant'), (60, 10))
    surface.blit(imgloader.loadimage('wateringcan'), (110, 10))
    surface.blit(imgloader.loadimage('shovel'), (160, 10))

def draw_seed(surface, seedid, position, imgloader):
        img = imgloader.loadimage('seed' + str(seedid))
        surface.blit(img, position)

def draw_selected_seed(surface, selectedseed, imgloader):
    if  selectedseed == None:return
    #draw selected seed
    img = imgloader.loadimage('dryground')
    surface.blit(img, (65, 65))
    draw_seed(surface, selectedseed, (65, 65), imgloader)

def render_seed_notify(surface, font, posx, posy, underseed, imgloader):
    """Render notification about planted seed"""

    sizex = 200
    sizey = 150
    posy += 5

    img = pygame.Surface((sizex, sizey))
    img.fill((48, 80, 80))
    pygame.draw.rect(img, (255, 255, 255), (0, 0, sizex - 1, sizey - 1), 1)

    #Draw seed
    draw_seed(img, underseed.id, (sizex / 2 - 32, 65), imgloader)

    #name
    text = "" + underseed.name + ""
    text = font.render(text, 0, (255, 255, 0), (255, 0, 255))
    text.set_colorkey((255, 0, 255))
    img.blit(text, (sizex / 2 - text.get_size()[0] / 2, 5))

    #remaining time
    text = "Complete in: " + underseed.remainstring
    text = font.render(text, 0, (255, 0, 100), (255, 0, 255))
    text.set_colorkey((255, 0, 255))
    img.blit(text, (sizex / 2 - text.get_size()[0] / 2, 25))

    #Quentity
    text = "Quantity:" + str(underseed.growquantity)
    text = font.render(text, 0, (255, 255, 150), (255, 0, 255))
    text.set_colorkey((255, 0, 255))
    img.blit(text, (sizex / 2 - text.get_size()[0] / 2, 45))

    #ready to harvest
    if underseed.to_harvest:
        text = font.render("Ready to Harvest", 0, (255, 255, 255), (255, 0, 255))
        text.set_colorkey((255, 0, 255))
        img.blit(text, (sizex / 2 - text.get_size()[0] / 2, sizey - 20))

    #alpha
    img.set_alpha(128 + 64)
    if posx > (640 - sizex):posx -= sizex
    surface.blit(img, (posx, posy))


def generate_field_sprites(imgloader, farmfield, farmoffset):
    group = pygame.sprite.OrderedUpdates()
    #background
    sprite = pygame.sprite.Sprite()
    sprite.image = imgloader['background']
    sprite.rect = (0, 0, 800, 600)
    group.add(sprite)

    for y in range(12):
        for x in range(12):
            farmtile = farmfield.get_farmtile(x, y)

            posx = (x - y) * 32 + farmoffset[0] + 150
            posy = (x + y) * 16 + farmoffset[1]

            #draw ground
            sprite = pygame.sprite.Sprite()
            sprite.rect = (posx, posy, 64, 32)
            if farmtile['water'] > 20:
                sprite.image = imgloader['wetground']
            else:
                sprite.image = imgloader['dryground']
            group.add(sprite)

            #draw plant or seed
            seed = farmtile['seed']

            if seed:
                sprite = pygame.sprite.Sprite()
                sprite.rect = (posx, posy, 64, 32)
                if not seed.to_harvest:
                    if not seed.wilted:
                        seed.update_remainig_growing_time()
                        #draw seeds on the ground
                        if seed.growtimeremaining <= 30 * 60:
                            sprite.image = imgloader['seedfullgrow']
                        elif seed.growtimeremaining <= 60 * 60:
                            sprite.image = imgloader['seedhalfgrow']

                        else:
                            sprite.image = imgloader['seed']
                    #seed is wilted
                    else:
                        sprite.image = imgloader['wiltedplant']
                else:
                    sprite.image = imgloader['seed' + str(seed.id)]
                #add sprite
                group.add(sprite)
    #return group object
    return group
