import pygame
from farmlib.seed import seeds

class PygameInventory:
    def __init__(self, imgloader):
        self.inventoryoffset = (10, 400)
        self.inventorysize = (5, 5)
        self.images = imgloader
        self.notifyfont = pygame.font.Font("droidsansmono.ttf", 12)

    def update(self):
        pass

    def render_inventory_notify(self, screenobj, posx, posy, index, player):
        """Render inventory notify"""

        sizex = 200
        sizey = 150

        img = pygame.Surface((sizex, sizey))
        img.fill((48, 80, 80))
        pygame.draw.rect(img, (255, 255, 255), (0, 0, sizex - 1, sizey - 1), 1)

        #Name
        text = seeds[index]['name'] + " x" + str(player.itemscounter[str(index)])
        text = self.notifyfont.render(text, 0, (255, 255, 0), (255, 0, 255))
        text.set_colorkey((255, 0, 255))
        img.blit(text, (sizex / 2 - text.get_size()[0] / 2, 5))

        #Descriptions
        text = self.notifyfont.render(seeds[index]['description'],
                                      0, (255, 0, 0), (255, 0, 255))
        text.set_colorkey((255, 0, 255))
        img.blit(text, (sizex / 2 - text.get_size()[0] / 2, 25))

        #alpha
        img.set_alpha(250)
        if posx > (640 - sizex):posx -= sizex
        screenobj.blit(img, (posx, posy))

    def draw_inventory_notify(self, surface, player):
        """"draw inventory notify window"""
        mx, my = pygame.mouse.get_pos()
        index = self.get_index_inventory_under_mouse()
        if index:
            itemid = index[1] * self.inventorysize[0] + index[0]
            if itemid < len(player.inventory):
                self.render_inventory_notify(surface, mx + 5, my + 10,
                    player.inventory[itemid], player)

    def get_index_inventory_under_mouse(self):
        """Get position of element in inventory under mouse cursor"""

        mx, my = pygame.mouse.get_pos()
        xx = (mx - self.inventoryoffset[0]) / 64
        yy = (my - self.inventoryoffset[1]) / 32

        if xx < 0 or yy < 0:return None
        if xx >= self.inventorysize[0]:return None
        if yy >= self.inventorysize[1]:return None
        xx = min(self.inventorysize[0] - 1, xx)
        yy = min(self.inventorysize[1] - 1, yy)
        return (xx, yy)

    def draw_inventory(self, surface, player):
        img = self.images['inventory']
        invpos = self.inventoryoffset[0], self.inventoryoffset[1] - 1
        surface.blit(img, invpos)
        #draw inv items
        counterx = 0
        countery = 0
        for item in player.inventory:
            surface.blit(self.images.loadimage('seed' + str(item)),
                (
                counterx * 64 + self.inventoryoffset[0],
                countery * 32 + self.inventoryoffset[1])
                )
            counterx += 1
            if counterx == self.inventorysize[0]:
                counterx = 0
                countery += 1
            if countery == self.inventorysize[1]:break
