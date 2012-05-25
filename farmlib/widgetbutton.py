import pygame

from widget import Widget

class Button(Widget):
    def __init__(self, label, position, bgimage = None, labelsize = 12,
                 color = (255, 255, 0)):
        self.bgimage = bgimage
        self.label = label
        self.color = color
        #self.image = image
        self.position = position
        self.labelsize = labelsize
        self.labelfont = pygame.font.Font("droidsansmono.ttf", self.labelsize)

        #Setup image
        if not self.bgimage:
            self._settextimage()
        else:
            self._setsize(self._calculate_size(self.bgimage))
        Widget.__init__(self, (self.width, self.height))

    def _render_text(self):
        return self.labelfont.render(self.label, 1, self.color)

    def _calculate_size(self, image):
        width = image.get_size()[0]
        height = image.get_size()[1]
        return (width, height)

    def _settextimage(self):
        self.image = self._render_text()
        self._setsize(self._calculate_size(self.image))


    def setimage(self, newimage):
        self.image = newimage
        self._setsize(self._calculate_size(self.image))

    def redraw(self, surface):
        if self.label and self.bgimage:
            img = self._render_text()
            surface.blit(img, self.position)
            surface.blit(self.bgimage, self.position)
        elif not self.bgimage:
            surface.blit(self.image, self.position)
        elif not self.label and self.bgimage:
            surface.blit(self.bgimage, self.position)

    def settext(self, newtext):
        self.text = newtext
        self.render_text()

    def _call_callback(self, signal):
        if signal in self.callbacks:
            if self.callbacks[signal]:
                self.callbacks[signal][0](self, **self.callbacks[signal][1])

    def poll_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = self.parent.get_relative_mousepos()
                if pos != None:
                    if pygame.Rect(self.position[0], self.position[1],
                                   self.width, self.height).collidepoint(pos):
                        self._call_callback("clicked")


