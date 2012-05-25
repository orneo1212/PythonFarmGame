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

        #items offset for gui buttons
        self.itemsoffset = [32, 20]

        #Create gui
        self.create_gui()


        #hide market at load
        self.hide()

    def create_gui(self):
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
        #Add images for seeds in market
        posx, posy = [0, 0]
        columns = (self.width / 64)
        rows = (self.height / 32)
        for seeddef in seeds:
            #add seed image widget 
            img = self.imgloader['seed' + str(seeddef['id'])]
            px = self.width / columns * posx + self.itemsoffset[0]
            py = self.height / rows * posy + self.itemsoffset[1]
            image = Image(img, (px, py))
            self.addwidget(image)
            posx += 1
            if posx > 1:
                posx = 0
                posy += 1
        #add buttons
        self.buybutton = Button("Buy", (80, 380))
        self.sellbutton = Button("Sell", (300, 380))
        self.addwidget(self.buybutton)
        self.addwidget(self.sellbutton)
        self.buybutton.connect("clicked", self.on_buy_clicked)
        self.sellbutton.connect("clicked", self.on_sell_clicked)

    def on_buy_clicked(self, widget, **data):
        self.player.money -= 5
        self.player.add_item(0)
        self.message.settext("You bought carrot")

    def on_sell_clicked(self, widget, **data):
        self.player.money += 5
        self.message.settext("You sold carrot")
