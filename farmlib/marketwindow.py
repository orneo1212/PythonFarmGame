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
        titlelabel = Label(
                           "Market place",
                           (200, 0),
                            size = 18,
                            color = (255, 255, 0),
                            align = "center")
        self.addwidget(titlelabel)

        #Add images for seeds in market
        posx, posy = [0, 0]
        offset = [32, 20]
        for seeddef in seeds:
            img = imgloader['seed' + str(seeddef['id'])]
            px = self.width / 2 * posx + offset[0]
            py = self.height / 6 * posy + offset[1]
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
        #hide market at load
        self.hide()

    def on_buy_clicked(self, widget, **data):
        self.player.money -= 5
        self.player.add_item(0)

    def on_sell_clicked(self, widget, **data):
        self.player.money += 5
