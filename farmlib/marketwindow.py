'''
Created on 24-05-2012

@author: orneo1212
'''
from __future__ import absolute_import

import pygame

import farmlib

from pygameui import Label, Image, Container, Button
from farmlib.farm import objects
from farmlib.tooltip import Tooltip

try:
    xrange
except NameError:
    xrange = range

WATERREFILLCOST = farmlib.rules["WATERREFILLCOST"]
OBJECTSNOTINMARKET = farmlib.rules["OBJECTSNOTINMARKET"]


class MarketWindow(Container):
    """Market Window

    """
    def __init__(self, width, height, imgloader, player, gamemanager):
        self.gamemanager = gamemanager
        self.player = player
        self.imgloader = imgloader
        Container.__init__(self, width, height, (200, 50))
        # set window alpha
        self.alphavalue = 250 * 0.95
        # items offset for gui buttons
        self.itemsoffset = [32, 20]
        # selected item
        self.selecteditem = None

        self.showborder = False

        # Selection count
        self.count = 1

        # Tooltip to draw
        self.tooltip = [None, None]

        # Create gui
        self.create_gui()

        # hide market at load
        self.hide()

    def create_gui(self):
        """Add images for seeds in market

        :return:
        """
        print('generate Marketwindow')
        posx, posy = [0, 0]
        columns = (self.width / 64) - 1
        # rows = (self.height / 32) - 1
        # Background
        bgimage = self.imgloader["marketbg"]
        bgimage = Image(bgimage, (0, 0))
        self.addwidget(bgimage)

        # close button
        closebutton = Button("X", (380, 3), labelsize=15,
                             color=(255, 255, 255))
        closebutton.connect("clicked", lambda x: self.hide())
        closebutton.connect("onshow", self.on_market_show)
        self.addwidget(closebutton)

        # refill watercan
        waterbuybutton = Button("Refill water (${0!s})".
                                format(WATERREFILLCOST),
                                (10, 30), color=(128, 128, 255))
        waterbuybutton.connect("clicked", self.on_water_buy)
        self.addwidget(waterbuybutton)

        # Buy farm
        farmcost = self.gamemanager.getnextfarmcost()
        self.buyfarm = Button("Buy new farm (${0!s})".format(farmcost),
                              (150, 30), color=(255, 0, 0))
        self.buyfarm.connect("clicked", self.on_farm_buy)
        self.addwidget(self.buyfarm)

        # Add items
        gridimg = self.imgloader['grid2']
        for seeddef in objects:
            if seeddef["id"] in OBJECTSNOTINMARKET:
                continue
            itemid = seeddef['id']
            # add seed image widget
            img = self.imgloader['object' + str(itemid)]
            px = 64 * posx + self.itemsoffset[0]
            py = 32 * posy + self.itemsoffset[1] + 30
            # add grid
            grid = Image(gridimg, (px, py))
            self.addwidget(grid)
            # Add image button
            imagebutton = Button("", (px, py), bgimage=img)
            self.addwidget(imagebutton)
            imagebutton.connect("clicked", self.on_item_select,
                                itemid=itemid)
            imagebutton.connect("onenter", self.on_mouse_item_enter,
                                itemid=itemid)
            imagebutton.connect("onleave", self.on_mouse_item_leave,
                                itemid=itemid)
            # limit
            posx += 1
            if posx >= columns:
                posx = 0
                posy += 1

        # Costlabel
        costlabel = Label("Cost:", (80, 340), size=12,
                          color=(255, 255, 255), align="center")
        self.addwidget(costlabel)
        # Cost value
        self.costvalue = Label("", (110, 340), size=12,
                               color=(200, 200, 50), align="center")
        self.addwidget(self.costvalue)

        # Selllabel
        selllabel = Label("Sell value:", (280, 340), size=12,
                          color=(255, 255, 255), align="center")
        self.addwidget(selllabel)
        # Sell value
        self.sellvalue = Label("", (330, 340), size=12,
                               color=(200, 200, 50), align="center")
        self.addwidget(self.sellvalue)

        # Message
        self.message = Label("", (10, 360), size=12,
                             color=(250, 0, 250), align="left")
        self.addwidget(self.message)
        # Selected item icon
        self.selectedicon = Image(None, (160, 332))
        self.addwidget(self.selectedicon)

        # add buttons
        self.buybutton = Button("BUY", (60, 370), color=(0, 255, 0),
                                labelsize=13)
        self.sellbutton = Button("SELL", (260, 375), color=(0, 255, 0),
                                 labelsize=13)
        self.addwidget(self.buybutton)
        self.addwidget(self.sellbutton)
        self.buybutton.connect("clicked", self.on_buy_clicked)
        self.sellbutton.connect("clicked", self.on_sell_clicked)

    def draw(self, surface):
        """draw

        :param surface:
        :return:
        """
        Container.draw(self, surface)
        if self.tooltip[0]:
            self.tooltip[0].draw(surface)

    def on_market_show(self, widget):
        """Reset market on show"""
        self.buybutton.settext("BUY")
        self.sellbutton.settext("SELL")
        self.message.settext("")
        self.selecteditem = None
        self.selectedicon.image = None
        self.sellvalue.settext("")
        self.costvalue.settext("")
        farmcost = self.gamemanager.getnextfarmcost()
        self.buyfarm.settext("Buy new farm (${0!s})".format(farmcost))

    def get_item_cost(self, itemid):
        """get item cost

        :param itemid:
        :return:
        """
        cost = int(objects[itemid]["price"])
        return cost * self.count

    def get_item_sell_value(self, itemid):
        """get item sell value

        :param itemid:
        :return:
        """
        sellcost = int(self.get_item_cost(itemid) / 8)
        return sellcost

    def update_buy_sell_button(self, itemid):
        """update buy sell button

        :param itemid:
        :return:
        """
        have = 0
        if self.player.item_in_inventory(itemid):
            have = self.player.itemscounter[str(itemid)]
        self.buybutton.settext("BUY x{0!s} (you have {1!s})".
                               format(str(self.count), have))
        self.sellbutton.settext("SELL x{0!s} ".format(str(self.count)))

    def on_item_select(self, widget, itemid):
        """selected item
        increase count if the same item selected

        :param widget:
        :param itemid:
        :return:
        """
        if itemid == self.selecteditem:
            self.count += 1
        else:
            self.count = 1

        self.selecteditem = itemid
        img = self.imgloader["object" + str(self.selecteditem)]
        # set image
        self.selectedicon.setimage(img)
        # update values
        cost = self.get_item_cost(itemid)
        self.costvalue.settext(cost)
        self.sellvalue.settext(self.get_item_sell_value(itemid))
        self.update_buy_sell_button(itemid)

    def on_buy_clicked(self, widget, **data):
        """buy clicked

        :param widget:
        :param data:
        :return:
        """
        if self.selecteditem is None:
            return
        itemid = self.selecteditem
        cost = self.get_item_cost(itemid)
        if self.player.money >= cost:
            self.player.money -= cost
            self.give_item(self.selecteditem, self.count)
            self.message.settext("You bought item")
            self.update_buy_sell_button(itemid)
        else:
            self.message.settext("You dont have enought money")

    def on_sell_clicked(self, widget, **data):
        """on sel clicked

        :param widget:
        :param data:
        :return:
        """
        if self.selecteditem is None:
            return
        itemid = self.selecteditem

        # remove item if player have it
        if self.player.item_in_inventory(itemid) \
                and self.player.itemscounter[str(itemid)] >= self.count:
            done = True
        else:
            done = False

        if done:
            # Remove items
            for x in xrange(self.count):
                self.player.remove_item(itemid)
            # Add money
            self.player.money += self.get_item_sell_value(itemid)
            self.message.settext("You sold item")
            self.update_buy_sell_button(itemid)
        else:
            self.message.settext("You don\'t have this item (or not enought)")

    def on_water_buy(self, widget, **data):
        """ water buy

        :param widget:
        :param data:
        :return:
        """
        if self.player.watercanuses == 100:
            self.message.settext("You no need refill")
            return
        if self.player.money >= WATERREFILLCOST:
            self.player.money -= WATERREFILLCOST
            self.player.watercanuses = 100
            self.message.settext("You filled watercan")
        else:
            self.message.settext("You dont have money to refill watercan")

    def give_item(self, itemid, count):
        """give item

        :param itemid:
        :param count:
        :return:
        """
        for x in xrange(count):
            self.player.add_item(self.selecteditem)

    # TOOLTIP
    def on_mouse_item_enter(self, widget, itemid):
        """on mouse item enter

        :param widget:
        :param itemid:
        :return:
        """
        seed = objects[itemid]
        otype = objects.get("type", "object")

        # Item is seed
        if otype == "seed":
            data = [
                    ["Name", seed["name"]],
                    ["Description", seed["description"]],
                    ["Quantity", str(seed["growquantity"])],
                    ["Grow in", str(seed["growtime"] / 60) + " minutes"],
                    ["Required level", str(seed.get("requiredlevel", 1))],
                    ]
        # Item is object
        else:
            data = [
                    ["Name", seed["name"]],
                    ["Description", seed["description"]],
                    ["Required level", str(seed.get("requiredlevel", 1))],
                    ]
        mx, my = pygame.mouse.get_pos()
        self.tooltip = [Tooltip((mx + 5, my + 5), data), widget]

    def on_mouse_item_leave(self, widget, itemid):
        """on mouse item leave

        :param widget:
        :param itemid:
        :return:
        """
        if self.tooltip[1] == widget:
            self.tooltip = [None, None]

    def on_farm_buy(self, widget):
        """on farm buy

        :param widget:
        :return:
        """
        farmcost = self.gamemanager.getnextfarmcost()
        if self.player.money < farmcost:
            self.message.settext("You dont have money to buy new farm")
        else:
            self.player.money -= farmcost
            self.gamemanager.addfarm()
            self.message.settext("You bought a new farm")
            self.on_market_show(None)
