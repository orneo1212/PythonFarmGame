'''
Created on 24-05-2012

@author: orneo1212
'''
from window import Window
from widgetlabel import Label
from widgetimage import Image
from widgetbutton import Button

from seed import seeds

class MarketWindow(Window):
    def __init__(self, size, imgloader, player):
        self.player = player
        self.imgloader = imgloader
        Window.__init__(self, size, (200, 40))
        #set window alpha
        self.alphavalue = 250 * 0.95
        #items offset for gui buttons
        self.itemsoffset = [32, 20]
        #selected item
        self.selecteditem = None

        self.showborder = False

        #Create gui
        self.create_gui()

        #hide market at load
        self.hide()

    def create_gui(self):
        #Add images for seeds in market
        posx, posy = [0, 0]
        columns = (self.width / 64) - 1
        rows = (self.height / 32) - 1
        #Background
        bgimage = self.imgloader["marketbg"]
        bgimage = Image(bgimage, (0, 0))
        self.addwidget(bgimage)

        #close button
        closebutton = Button("X", (380, 0), labelsize = 15, \
                             color = (255, 255, 255))
        closebutton.connect("clicked", lambda x:self.hide())
        self.addwidget(closebutton)

        #Add items
        gridimg = self.imgloader['grid2']
        for seeddef in seeds:
            itemid = seeddef['id']
            #add seed image widget
            img = self.imgloader['seed' + str(itemid)]
            px = 64 * posx + self.itemsoffset[0]
            py = 32 * posy + self.itemsoffset[1]
            #add grid
            grid = Image(gridimg, (px, py))
            self.addwidget(grid)
            #Add image button
            imagebutton = Button("", (px, py), bgimage = img)
            self.addwidget(imagebutton)
            imagebutton.connect("clicked", self.on_item_select, itemid = itemid)
            #limit
            posx += 1
            if posx >= columns:
                posx = 0
                posy += 1

        #Title
        titlelabel = Label("Market place", (200, 0), size = 18,
                           color = (255, 255, 0), align = "center")
        self.addwidget(titlelabel)


        #===================
        # DRAW ITEM DETAILS
        #===================

        #Costlabel
        costlabel = Label("Cost:", (80, 340), size = 12,
                           color = (255, 255, 255), align = "center")
        self.addwidget(costlabel)
        #Cost value
        self.costvalue = Label("", (100, 340), size = 12,
                           color = (200, 200, 50), align = "center")
        self.addwidget(self.costvalue)

        #Selllabel
        selllabel = Label("Sell value:", (280, 340), size = 12,
                           color = (255, 255, 255), align = "center")
        self.addwidget(selllabel)
        #Sell value
        self.sellvalue = Label("", (320, 340), size = 12,
                           color = (200, 200, 50), align = "center")
        self.addwidget(self.sellvalue)

        #Name label
        namelabel = Label("Name:", (80, 300), size = 12,
                           color = (255, 255, 255), align = "center")
        self.addwidget(namelabel)
        #Name value
        self.namevalue = Label("", (100, 300), size = 12,
                           color = (200, 200, 50), align = "center")
        self.addwidget(self.namevalue)

        #Quantity label
        quantitylabel = Label("Quantity:", (80, 320), size = 12,
                           color = (255, 255, 255), align = "center")
        self.addwidget(quantitylabel)
        #Quantity value
        self.quantityvalue = Label("", (120, 320), size = 12,
                           color = (200, 200, 50), align = "center")
        self.addwidget(self.quantityvalue)

        #grow label
        growlabel = Label("Grow in: ", (280, 320), size = 12,
                           color = (255, 255, 255), align = "center")
        self.addwidget(growlabel)
        #grow value
        self.growvalue = Label("", (320, 320), size = 12,
                           color = (200, 200, 50), align = "center")
        self.addwidget(self.growvalue)

        #Message
        self.message = Label("", (10, 360), size = 12,
                           color = (250, 0, 250), align = "center")
        self.addwidget(self.message)
        #Selected item icon
        self.selectedicon = Image(None, (160, 332))
        self.addwidget(self.selectedicon)

        #add buttons
        self.buybutton = Button("Buy", (60, 380), color = (0, 255, 0))
        self.sellbutton = Button("Sell", (300, 380), color = (0, 255, 0))
        self.addwidget(self.buybutton)
        self.addwidget(self.sellbutton)
        self.buybutton.connect("clicked", self.on_buy_clicked)
        self.sellbutton.connect("clicked", self.on_sell_clicked)

    def get_item_cost(self, itemid):
        cost = int(seeds[itemid]["price"])
        return cost

    def get_item_sell_value(self, itemid):
        sellcost = int(self.get_item_cost(itemid) / 8)
        return sellcost

    def update_buy_sell_button(self, itemid):
        have = 0
        if self.player.item_in_inventory(itemid):
            have = self.player.itemscounter[str(itemid)]
        self.buybutton.settext("Buy (%s)" % have)
        self.sellbutton.settext("Sell (%s)" % have)

    def on_item_select(self, widget, itemid):
        self.selecteditem = itemid
        img = self.imgloader["seed" + str(self.selecteditem)]
        #set image
        self.selectedicon.setimage(img)
        #update values
        cost = self.get_item_cost(itemid)
        self.costvalue.settext(cost)
        self.sellvalue.settext(self.get_item_sell_value(itemid))
        self.namevalue.settext(seeds[itemid]["name"])
        self.quantityvalue.settext(str(seeds[itemid]["growquantity"]))
        self.growvalue.settext(str(seeds[itemid]["growtime"] / 60) + " min")
        self.update_buy_sell_button(itemid)

    def on_buy_clicked(self, widget, **data):
        if self.selecteditem is None:return
        itemid = self.selecteditem
        cost = self.get_item_cost(itemid)
        if self.player.money >= cost:
            self.player.money -= cost
            self.player.add_item(self.selecteditem)
            self.message.settext("You bought item")
            self.update_buy_sell_button(itemid)
        else:
            self.message.settext("You dont have enought money")

    def on_sell_clicked(self, widget, **data):
        if self.selecteditem is None:return
        itemid = self.selecteditem

        #remove item if player have it
        done = self.player.remove_item(itemid)
        if done:
            self.player.money += self.get_item_sell_value(itemid)
            self.message.settext("You sold item")
            self.update_buy_sell_button(itemid)
        else:
            self.message.settext("You don\'t have this item")
