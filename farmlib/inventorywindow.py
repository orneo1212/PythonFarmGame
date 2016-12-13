from __future__ import absolute_import

import base64

import pygame

from farmlib.farm import objects
from pygameui import Label, Button, Container, Image
from farmlib.tooltip import Tooltip


class InventoryWindow(Container):
    """Inventory Window

    """
    def __init__(self, imgloader, player):
        Container.__init__(self, 400, 500, (200, 50))
        self.inventoryoffset = (0, 10)
        self.inventorysize = (4, 5)
        self.images = imgloader
        self.player = player
        self.notifyfont = pygame.font.Font("dejavusansmono.ttf", 12)

        # tooltip
        self.tooltip = [None, None]

        # Last checksum
        self.lchecksum = ""

        self.create_gui()

    def ismodified(self):
        """Return True when inventory was been modified (based on checksum)"""
        try:
            checksum = base64.b64encode(str(self.player.inventory))
            checksum = base64.b64encode(
                    checksum + str(self.player.itemscounter))
        except TypeError:
            checksum = base64.b64encode(bytes(self.player.inventory))
            checksum = base64.b64encode(
                    checksum + bytes(str(self.player.itemscounter).encode()))

        if checksum != self.lchecksum:
            self.lchecksum = checksum
            return True
        else:
            return False

    def draw(self, surface):
        """Override Window draw function"""
        Container.draw(self, surface)
        if self.tooltip[0]:
            self.tooltip[0].draw(surface)

    def create_gui(self):
        """create gui

        :return:
        """
        self.remove_all_widgets()
        bg = Image(self.images['inventory'], (0, 0))
        self.addwidget(bg)

        # close button
        closebutton = Button("X", (380, 3), labelsize=15,
                             color=(255, 255, 255))
        closebutton.connect("clicked", lambda x: self.hide())
        self.addwidget(closebutton)

        # create items
        counterx = 0
        countery = 0
        for item in self.player.inventory:
            px = counterx * 64 + self.inventoryoffset[0] + 25
            py = countery * 32 + self.inventoryoffset[1] + 30
            # make grid
            px += counterx * 30
            py += countery * 15

            # grid image
            gridimage = Image(self.images['grid2'], (px, py))
            self.addwidget(gridimage)

            # item button
            img = self.images['object' + str(item)]
            itembutton = Button("", (px, py), img)
            itembutton.connect("clicked",
                               self.on_item_select, itemid=item)
            itembutton.connect("onenter",
                               self.on_item_enter, itemid=item)
            itembutton.connect("onleave", self.on_item_leave)
            self.addwidget(itembutton)

            # item count
            text = str(self.player.itemscounter[str(item)])
            itemcount = Label(text, (px + 40, py + 16), align="center")
            self.addwidget(itemcount)

            # limit
            counterx += 1
            if counterx == self.inventorysize[0]:
                counterx = 0
                countery += 1
            if countery == self.inventorysize[1]:
                break

    def on_item_enter(self, widget, itemid):
        """on item enter

        :param widget:
        :param itemid:
        :return:
        """
        seed = objects[itemid]
        otype = objects.get("type", "object")

        # this is seed
        if otype == "seed":
            data = [
                    ["Name", seed["name"]],
                    ["Description", seed["description"]],
                    ["Quantity", str(seed["growquantity"])],
                    ["Grow in", str(seed["growtime"] / 60) + " minutes"],
                    ["Required level", str(seed.get("requiredlevel", 1))],
                    ]
        # this is object
        else:
            data = [
                    ["Name", seed["name"]],
                    ["Description", seed["description"]],
                    ["Required level", str(seed.get("requiredlevel", 1))],
                    ]
        mx, my = pygame.mouse.get_pos()
        self.tooltip = [Tooltip((mx + 5, my + 5), data), widget]

    def on_item_leave(self, widget):
        """on item leave
        remove itemid
        :param widget:
        :return:
        """
        if self.tooltip[1] == widget:
            self.tooltip = [None, None]

    def repaint(self):
        """repaint

        :return:
        """
        Container.repaint(self)
        # self.create_gui()
        # Mark widgets not modified
        for widget in self.widgets:
            widget.mark_modified(False)

    def get_index_inventory_under_mouse(self):
        """
        Get position of element in inventory under mouse cursor
        """
        mx, my = pygame.mouse.get_pos()
        xx = (mx - self.inventoryoffset[0]) / 64
        yy = (my - self.inventoryoffset[1]) / 32

        if xx < 0 or yy < 0:
            return None
        if xx >= self.inventorysize[0]:
            return None
        if yy >= self.inventorysize[1]:
            return None
        xx = min(self.inventorysize[0] - 1, xx)
        yy = min(self.inventorysize[1] - 1, yy)
        return (xx, yy)

    def on_item_select(self, widget, itemid):
        """on item select

        :param itemid:
        :return:
        """
        self.player.selecteditem = itemid
        self.player.selectedtool = "plant"
