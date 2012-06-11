import pygame

from farmlib.farmobject import objects
from pygameui import Label, Button, Window, Image

class InventoryWindow(Window):
    def __init__(self, imgloader, player):
        Window.__init__(self, (328, 168), (10, 400))
        self.inventoryoffset = (10, 10)
        self.inventorysize = (5, 5)
        self.images = imgloader
        self.player = player
        self.notifyfont = pygame.font.Font("dejavusansmono.ttf", 12)
        self.create_gui()

    def create_gui(self):
        self.remove_all_widgets()
        bg = Image(self.images['inventory'], (0, 0))
        self.addwidget(bg)

        #create items
        counterx = 0
        countery = 0
        for item in self.player.inventory:
            px = counterx * 64 + self.inventoryoffset[0] + 4
            py = countery * 32 + self.inventoryoffset[1] + 2

            #grid image
            gridimage = Image(self.images['grid2'], (px, py))
            self.addwidget(gridimage)

            #item button
            itembutton = Button("", (px, py), self.images['object' + str(item)])
            itembutton.connect("clicked", self.on_item_select, itemid = item)
            self.addwidget(itembutton)

            #item count
            text = str(self.player.itemscounter[str(item)])
            itemcount = Label(text, (px + 40, py + 16), align = "center")
            self.addwidget(itemcount)

            #limit
            counterx += 1
            if counterx == self.inventorysize[0]:
                counterx = 0
                countery += 1
            if countery == self.inventorysize[1]:break

    def repaint(self):
        Window.repaint(self)
        self.create_gui()
        #Mark widgets not modified
        for widget in self.widgets:
            widget.mark_modified(False)

    def render_inventory_notify(self, screenobj, posx, posy, index, player):
        """Render inventory notify"""
        #TODO: remove this
        sizex = 250
        sizey = 150

        img = pygame.Surface((sizex, sizey))
        img.fill((48, 80, 80))
        pygame.draw.rect(img, (255, 255, 255), (0, 0, sizex - 1, sizey - 1), 1)

        #Name
        text = objects[index]['name'] + " x" + str(player.itemscounter[str(index)])
        text = self.notifyfont.render(text, 0, (255, 255, 0), (255, 0, 255))
        text.set_colorkey((255, 0, 255))
        img.blit(text, (sizex / 2 - text.get_size()[0] / 2, 5))

        #Descriptions
        text = self.notifyfont.render(objects[index]['description'],
                                      0, (255, 0, 0), (255, 0, 255))
        text.set_colorkey((255, 0, 255))
        img.blit(text, (sizex / 2 - text.get_size()[0] / 2, 25))

        if objects[index].get("growquantity", 0):

            #grow quantity
            harvestcount = objects[index].get('harvestcount', 1)
            text = "Quantity: %s (%s)" % (str(objects[index]['growquantity']),
                                          str(harvestcount))
            text = self.notifyfont.render(text,
                    0, (255, 255, 150), (255, 0, 255))
            text.set_colorkey((255, 0, 255))
            img.blit(text, (sizex / 2 - text.get_size()[0] / 2, 45))

            #Required level
            requiredlevel = objects[index].get('requiredlevel', 1)
            text = self.notifyfont.render("Required level: %s" % requiredlevel,
                                          0, (255, 255, 150), (255, 0, 255))
            text.set_colorkey((255, 0, 255))
            img.blit(text, (sizex / 2 - text.get_size()[0] / 2, 65))

        #Draw object
        objectimg = self.images["object" + str(index)]
        img.blit(objectimg, (sizex / 2 - 32, 85))

        #alpha
        img.set_alpha(200)
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

    def on_item_select(self, widget, itemid):
        self.player.selecteditem = itemid
        self.player.selectedtool = "plant"
