import pygame

from widget import Widget

class Button(Widget):
    def __init__(self, label, position, bgimage = None, labelsize = 12,
                 labelcolor = (255, 255, 0)):
        self.bgimage = bgimage
        self.label = label
        self.color = labelcolor
        #self.image = image
        self.position = position
        self.labelsize = labelsize
        self.labelfont = pygame.font.Font("droidsansmono.ttf", self.labelsize)

        #Setup image
        if not self.bgimage:
            self.render_text()
        else:
            self.width = self.bgimage.get_size()[0]
            self.height = self.bgimage.get_size()[1]
        Widget.__init__(self, (self.width, self.height))

    def render_text(self):
        self.image = self.labelfont.render(self.label, 1, self.color)
        self.width = self.image.get_size()[0]
        self.height = self.image.get_size()[1]

    def setimage(self, newimage):
        self.image = newimage

    def redraw(self, surface):
        surface.blit(self.image, self.position)

    def settext(self, newtext):
        self.text = newtext
        self.render_text()

    def _call_callback(self, signal, callback, data = {}):
        print "clicked"
        if signal in self.callbacks:
            if self.callbacks[signal]:
                self.callbacks[signal](self, **data)

    def poll_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                kx, ky = event.pos
                if pygame.Rect(self.position[0], self.position[1],
                               self.width, self.height).collidepoint(kx, ky):
                    self._call_callback((kx, ky))


