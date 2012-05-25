import pygame

from widget import Widget

class Label(Widget):
    def __init__(self, text, position, size = 12,
            color = (255, 255, 255), align = "left"):
        self.text = text
        self.labelfont = pygame.font.Font("droidsansmono.ttf", size)
        self.image = None
        self.color = color
        self.position = position
        self.align = align

        #set width and height
        self.render_text()
        self.width = self.image.get_size()[0]
        self.height = self.image.get_size()[1]
        self.setposition(self.position)
        Widget.__init__(self, (self.width, self.height))

    def render_text(self):
        self.image = self.labelfont.render(self.text, 1, self.color)
        self.width = self.image.get_size()[0]
        self.height = self.image.get_size()[1]

    def setposition(self, position):
        if self.align == "center":
            position = position[0] - self.width / 2, position[1]
        self.position = position

    def redraw(self, surface):
        surface.blit(self.image, self.position)

    def settext(self, newtext):
        newtext = unicode(newtext)
        self.text = newtext
        self.render_text()