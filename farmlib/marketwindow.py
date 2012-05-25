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
        Window.__init__(self, size, (350, 40))
        #set window alpha
        self.alphavalue = 250 * 0.85
        #items offset for gui buttons
        self.itemsoffset = [32, 20]
        #selected item
        self.selecteditem = None

        #Create gui
        self.create_gui()

        #hide market at load
        self.hide()

    def create_gui(self):
        #Add images for seeds in market
        posx, posy = [0, 0]
        columns = (self.width / 64)
        rows = (self.height / 32)
        for seeddef in seeds:
            itemid = seeddef['id']
            #add seed image widget 
            img = self.imgloader['seed' + str(itemid)]
            px = self.width / columns * posx + self.itemsoffset[0]
            py = self.height / rows * posy + self.itemsoffset[1]
            imagebutton = Button("", (px, py), bgimage = img)
            self.addwidget(imagebutton)
            imagebutton.connect("clicked", self.on_item_select, itemid = itemid)
            posx += 1
            if posx > columns:
                posx = 0
                posy += 1
        #Title 
        titlelabel = Label("Market place", (200, 0), size = 18,
                           color = (255, 255, 0), align = "center")
        self.addwidget(titlelabel)
        #Costlabel
        costlabel = Label("Buy cost:", (80, 340), size = 12,
                           color = (200, 0, 200), align = "center")
        self.addwidget(costlabel)
        #Cost value
        self.costvalue = Label("0", (120, 340), size = 12,
                           color = (200, 200, 50), align = "center")
        self.addwidget(self.costvalue)
        #Message
        self.message = Label("", (10, 360), size = 12,
                           color = (255, 0, 255), align = "center")
        self.addwidget(self.message)
        #Selected item icon
        self.selectedicon = Image(None, (0, 332))
        self.addwidget(self.selectedicon)

        #add buttons
        self.buybutton = Button("Buy", (80, 380), color = (0, 255, 0))
        self.sellbutton = Button("Sell", (300, 380), color = (0, 255, 0))
        self.addwidget(self.buybutton)
        self.addwidget(self.sellbutton)
        self.buybutton.connect("clicked", self.on_buy_clicked)
        self.sellbutton.connect("clicked", self.on_sell_clicked)

    def on_item_select(self, widget, itemid):
        self.selecteditem = itemid
        img = self.imgloader["seed" + str(self.selecteditem)]
        self.selectedicon.setimage(img)
        cost = seeds[itemid]["growtime"]
        self.costvalue.settext(cost)

    def on_buy_clicked(self, widget, **data):
        if self.player.money >= 5:
            self.player.money -= 5
            self.player.add_item(self.selecteditem)
            self.message.settext("You bought item")
        else:
            self.message.settext("You dont have enought money")

    def on_sell_clicked(self, widget, **data):
        if self.selecteditem is None:return
        itemid = self.selecteditem

        #remove item if player have it
        done = self.player.remove_item(itemid)
        if done:
            self.player.money += seeds[itemid]["growtime"] / 2
            self.message.settext("You sold item")
        else:
            self.message.settext("You don\'t have this item")
