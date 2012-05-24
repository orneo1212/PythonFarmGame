from widget import Widget

class Image(Widget):
    def __init__(self, image, position):
        self.image = image
        self.position = position

        #set width and height
        self.width = self.image.get_size()[0]
        self.height = self.image.get_size()[1]
        Widget.__init__(self, (self.width, self.height))

    def setimage(self, newimage):
        self.image = newimage

    def redraw(self, surface):
        surface.blit(self.image, self.position)
